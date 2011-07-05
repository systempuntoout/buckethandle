import logging, web, re
import urlparse
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.ext import deferred
import app.utility.worker as worker
from google.appengine.api.taskqueue import taskqueue
import app.db.models as models
import app.db.counter as counter
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
        elif action =='start_import':
            taskqueue.add(url='/admin?action=import',
                          method = 'GET', 
                          queue_name = 'populate',
                          countdown = 5)
        elif action =='import':
            fi = open('app/data/import.txt')
            for line in fi:
                splitted_data = line.strip().split(';')
                try:
                    url_img = splitted_data[4].strip()
                except:
                    url_img = ''
                    
                taskqueue.add(url='/admin',
                              method = 'POST', 
                              queue_name = 'populate',
                              countdown = 5,
                              params = {
                                'action' : 'newpost',
                                'title': splitted_data[0],
                                'link' : splitted_data[1],
                                'category' : splitted_data[2],
                                'tags' : splitted_data[3].strip(),
                                'url_img': url_img
                              })
        elif action =='populate':
            timestamp = utils.generate_key_name()
            title= u"Title test %s" % timestamp
            link = "http://www.foo.it"
            description= "Description test %s" % timestamp
            body = "test"
            tags = ""
            for tag in range(random.randint(1,5)):
                tagindex = random.randint(1,500)
                tags = tags + " foo%s" % tagindex
            tags = [tag.lower() for tag in tags.split()]
            category = CATEGORIES[random.randint(0,6)]
            post = models.Post(key_name = utils.inverse_microsecond_str(),
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
            counter.increment("Posts_Count")
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
            base_link = utils.get_base_link(link)
            if base_link in AUTO_CONTENT_BY_LINK:
                if 'category' in AUTO_CONTENT_BY_LINK[base_link]:
                    selected_category = AUTO_CONTENT_BY_LINK[base_link]['category']
                else:
                    selected_category = ''
            else: 
                selected_category = ''
                
            tags = list(set(tags.split()) - set(TAGS_BLACK_LIST))
            return render.layout(render.admin(result, title, link, description, tags, selected_category), title ='Admin', navbar = False, user = users.get_current_user(), is_user_admin = users.is_current_user_admin())
        elif action =='newpost':
            title = web.input(title = None)['title']
            link = web.input(link = None)['link']
            description = web.input(description = None)['description']
            tags = web.input(tags = None)['tags']
            category = web.input(category = None)['category']
            body = web.input(body = None)['body']
            featured = web.input(featured = False)['featured']
            thumbnail = web.input(img = None)['img']
            thumbnail_url = web.input(url_img = None)['url_img']
            if thumbnail_url:
                response = urlfetch.fetch(url=thumbnail_url,
                               method=urlfetch.GET,
                               deadline = 10)
                thumbnail = response.content
            
            if thumbnail:
                thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                blob_thumbnail= db.Blob(thumbnail)
            else:
                blob_thumbnail= None
            
            if link:
                link_for_db = db.Link(link)
            else:
                link_for_db= None
            
            tags = list(set([tag.lower() for tag in tags.split()])- set(TAGS_BLACK_LIST))
            
            post = models.Post(key_name = utils.inverse_microsecond_str(),
                               title = title,
                               link = link_for_db,
                               description = description,
                               tags = tags,
                               category = category,
                               thumbnail = blob_thumbnail,
                               slug = utils.slugify(title),
                               author_name = AUTHOR_NAME,
                               featured = True if featured else False,
                               body = body  )
            
            result['newpost'] = post.put()
            counter.increment("Posts_Count")
            deferred.defer(worker.deferred_update_tags_counter,tags)
            deferred.defer(worker.deferred_update_category_counter,category)
        elif action =='editpost_init':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity = models.Post.get(post_id)
                if entity:
                    return render.layout(render.admin(result,
                                                      entity.title,
                                                      entity.link, 
                                                      entity.description, 
                                                      entity.tags,
                                                      entity.category,
                                                      entity.get_image_path(),
                                                      entity.body,
                                                      post_id, entity.featured), title ='Admin', navbar = False, user = users.get_current_user(), is_user_admin = users.is_current_user_admin())
            result ={'Not_found':post_id}
            render.layout(render.admin(result), title ='Admin', navbar = False, user = users.get_current_user(), is_user_admin = users.is_current_user_admin())
        elif action =='editpost':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity_post = models.Post.get(post_id)
                tags_old = entity_post.tags
                category_old = entity_post.category
                title = web.input(title = None)['title']
                link = web.input(link = None)['link']
                description = web.input(description = None)['description']
                tags = web.input(tags = None)['tags']
                category = web.input(category = None)['category']
                body = web.input(body = None)['body']
                featured = web.input(featured = False)['featured']
                thumbnail = web.input(img = None)['img']
                delete_img = web.input(delete_img = None)['delete_img']
                thumbnail_url = web.input(url_img = None)['url_img']

                if thumbnail_url:
                    response = urlfetch.fetch(url=thumbnail_url,
                                   method=urlfetch.GET,
                                   deadline = 10)
                    thumbnail = response.content
                if thumbnail:
                    thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                    blob_thumbnail= db.Blob(thumbnail)
                else:
                    blob_thumbnail= None
                
                if link:
                    link_for_db = db.Link(link)
                else:
                    link_for_db= None
                
                tags = list(set([tag.lower() for tag in tags.split()])- set(TAGS_BLACK_LIST))
            
                entity_post.title = title
                entity_post.link = link_for_db
                entity_post.description = description
                entity_post.tags = tags
                entity_post.category = category
                entity_post.slug = utils.slugify(title)
                entity_post.body = body
                entity_post.featured = True if featured else False
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
                entity = models.Post.get(post_id)
                if entity:
                    result['delete_post'] = entity.delete()
                    counter.decrement("Posts_Count")
                    worker.deferred_update_tags_counter([],entity.tags)
                    worker.deferred_update_category_counter(None, entity.category)
        
        return render.layout(render.admin(result), title ='Admin', navbar = False, user = users.get_current_user(), is_user_admin = users.is_current_user_admin())

        
class Warmup:
    """
    Warming Requests for avoiding latency
    """
    def GET(self):
        pass