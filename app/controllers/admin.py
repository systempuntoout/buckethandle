import logging, web, re
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.ext import deferred
import app.utility.worker as worker
from google.appengine.api.taskqueue import taskqueue
import app.db.models as models
import app.utility.utils as utils
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import images
from app.config.settings import *
import random

render = web.render

class Admin:
    """
    Admin homepage
    """
    def POST(self):
        return self.GET()
        
    def GET(self):
        result = {}
        posts = []
        tags_filter = []
        action = web.input(action = None)['action']
        if action =='filter':
            tags_filter = web.input(title = None)['tags'].split()
        elif action =='memcachestats':
            result = memcache.get_stats()        
        elif action =='memcacheflush':
            result['result'] = memcache.flush_all()
        elif action =='populate':
            key_name = utils.generate_key_name()
            title= u"Title test %s" % key_name
            link = "http://www.foo.it"
            description= "Description test %s" % key_name
            body = "test"
            tags = ""
            for tag in range(random.randint(1,5)):
                tagindex = random.randint(1,50)
                tags = tags + " foo%s" % tagindex
            tags = [tag.lower() for tag in tags.split()]
            category = CATEGORIES[random.randint(0,6)]
            post = models.Post(key_name = key_name,
                               title = title,
                               link = db.Link(link),
                               description = description,
                               tags = tags,
                               category = category,
                               thumbnail = None,
                               slug = utils.slugify(title),
                               author_name = 'test',
                               body = body  )
            
            post.put()
            deferred.defer(worker.deferred_update_tags_counter,tags)
            deferred.defer(worker.deferred_update_category_counter,category)
            taskqueue.add(url='/admin?action=populate', 
                          method = 'GET', 
                          queue_name = 'populate',
                          countdown = 5)
            
        elif action =='newpost_init':
            title = web.input(title = '')['title']
            link = web.input(link = '')['link']
            description = web.input(description = '')['description']
            tags = web.input(tags = '')['tags']
            return render.layout(render.admin(result, title, link, description, tags.split()), title ='Admin', navbar = False, admin = users.get_current_user())
        elif action =='newpost':
            title = web.input(title = None)['title']
            link = web.input(link = None)['link']
            description = web.input(description = None)['description']
            tags = web.input(tags = None)['tags']
            category = web.input(category = None)['category']
            body = web.input(body = None)['body']
            thumbnail = web.input(img = None)['img']
            
            if thumbnail:
                thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                blob_thumbnail= db.Blob(thumbnail)
            else:
                blob_thumbnail= None
            
            tags = [tag.lower() for tag in tags.split()]
            
            post = models.Post(key_name = utils.generate_key_name(),
                               title = title,
                               link = db.Link(link),
                               description = description,
                               tags = tags,
                               category = category,
                               thumbnail = blob_thumbnail,
                               slug = utils.slugify(title),
                               author_name = users.get_current_user().nickname(),
                               body = body  )
            
            result['newpost'] = post.put()
            deferred.defer(worker.deferred_update_tags_counter,tags)
            deferred.defer(worker.deferred_update_category_counter,category)
        elif action =='editpost_init':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity = models.Post.get_by_key_name(post_id)
                if entity:
                    return render.layout(render.admin(result,
                                                      entity.title,
                                                      entity.link, 
                                                      entity.description, 
                                                      entity.tags,
                                                      entity.category,
                                                      entity.get_image_path(),
                                                      entity.body,
                                                      post_id), title ='Admin', navbar = False, admin = users.get_current_user())
            result ={'Not_found':post_id}
            render.layout(render.admin(result), title ='Admin', navbar = False, admin = users.get_current_user())
        elif action =='editpost':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity_post = models.Post.get_by_key_name(post_id)
                tags_old = entity_post.tags
                category_old = entity_post.category
                title = web.input(title = None)['title']
                link = web.input(link = None)['link']
                description = web.input(description = None)['description']
                tags = web.input(tags = None)['tags']
                category = web.input(category = None)['category']
                body = web.input(body = None)['body']
                thumbnail = web.input(img = None)['img']
                delete_img = web.input(delete_img = None)['delete_img']
                if thumbnail:
                    thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                    blob_thumbnail= db.Blob(thumbnail)
                else:
                    blob_thumbnail= None
            
                tags = [tag.lower() for tag in tags.split()]
            
                entity_post.title = title
                entity_post.link = db.Link(link)
                entity_post.description = description
                entity_post.tags = tags
                entity_post.category = category
                entity_post.slug = utils.slugify(title)
                entity_post.body = body
                if blob_thumbnail:
                    entity_post.thumbnail = blob_thumbnail
                if delete_img:
                    entity_post.thumbnail = None            
                result['editpost'] = entity_post.put()
                worker.deferred_update_tags_counter(entity_post.tags, tags_old)
                worker.deferred_update_category_counter(entity_post.category, category_old)
        elif action =='deletepost':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity = models.Post.get_by_key_name(post_id)
                if entity:
                    result['delete_post'] = entity.delete()
                    worker.deferred_update_tags_counter([],entity.tags)
                    worker.deferred_update_category_counter(None, entity.category)
        
        return render.layout(render.admin(result), title ='Admin', navbar = False, admin = users.get_current_user())

        
class Warmup:
    """
    Warming Requests for avoiding latency
    """
    def GET(self):
        pass