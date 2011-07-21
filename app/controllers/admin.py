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


def render_template(submitted, result, action, **kwargs):
    """
     Renders the layout template for the admin
    """

    return render.layout(render.admin(submitted, 
                                      result, 
                                      action, 
                                      **kwargs), 
                                      title ='Admin', 
                                      navbar = False, 
                                      user = users.get_current_user(), 
                                      is_user_admin = users.is_current_user_admin())
                          

class Admin:
    """
    Admin homepage
    """
    def POST(self):
        return self.GET()
        
    def GET(self):
        result = {}
        posts = []
        submitted = True
        tags_filter = []
        action = web.input(action = None)['action']
        if action =='memcachestats':
            result = memcache.get_stats()        
        elif action =='memcacheflush':
            result['result'] = memcache.flush_all()
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
            category = CATEGORIES[random.randint(0,5)]
            post = models.Post(key_name = utils.inverse_microsecond_str(),
                               title = title,
                               link = db.Link(link),
                               description = description,
                               tags = tags,
                               category = category,
                               thumbnail = None,
                               slug = utils.slugify(title),
                               author_name = 'test',
                               body = body )
            post.put()
            counter.increment("Posts_Count")
            deferred.defer(worker.deferred_update_tags_counter,tags)
            deferred.defer(worker.deferred_update_category_counter,category)
            taskqueue.add(url='/admin?action=populate',
                         method = 'GET',
                         queue_name = 'populate',
                         countdown = 5)
        elif action =='start_sitemapize':
            taskqueue.add(url='/admin?action=sitemapize',
                          method = 'GET', 
                          queue_name = 'populate',
                          countdown = 5)
            result[action] = "Done"
        elif action =='sitemapize': #Create sitemap archives
            entities = models.Post.all(keys_only = True).order("created")
            keys = []
            for entity in entities:
                keys.insert(0, str(entity))
                if len(keys) >= POSTS_PER_SITEMAP:
                    sitemap = models.Sitemap()
                    sitemap.post_count = POSTS_PER_SITEMAP
                    sitemap.post_keys = keys
                    sitemap.archived = True
                    posts = models.Post.get(keys)
                    sitemap.content = unicode(render.sitemap_posts(posts))
                    sitemap.put()
                    keys = []
            if keys:
                sitemap = models.Sitemap()
                sitemap.post_count = len(keys)
                sitemap.post_keys = keys
                sitemap.put()
                 
            
        elif action =='start_import':
            taskqueue.add(url='/admin?action=import',
                          method = 'GET', 
                          queue_name = 'populate',
                          countdown = 5)
            result[action] = "Done"
        elif action =='import': #Import from archive
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
            return render_template(True, 
                                   result, 
                                   action, 
                                   title = title,
                                   link = link,
                                   description = description,
                                   tags = tags,
                                   category = selected_category
                                   )
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

            #Various checks
            if not title:
                result[action] = "Please fill in all required fields (*)"
                submitted = False
            if link and not utils.link_is_valid(link):
                result[action] = "Link is not valid"
                submitted = False
            if thumbnail and thumbnail_url:
                result[action] = "Only one kind of img is allowed"
                submitted = False
            if thumbnail_url and not utils.link_is_valid(thumbnail_url):
                result[action] = "url_img is not a valid URL"
                submitted = False
            if not submitted:
                return render_template(submitted, 
                                       result, 
                                       action, 
                                       title = title,
                                       link = link,
                                       description = description,
                                       tags = tags.split(),
                                       category = category,
                                       body = body,
                                       url_img = thumbnail_url,
                                       featured = featured
                                       )
            #Preparing for datastore
            if thumbnail_url:
                response = urlfetch.fetch(url=thumbnail_url,
                               method=urlfetch.GET,
                               deadline = 10)
                thumbnail = response.content
            if thumbnail:
                thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                thumbnail_for_db= db.Blob(thumbnail)
            else:
                thumbnail_for_db= None
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
                               thumbnail = thumbnail_for_db,
                               slug = utils.slugify(title),
                               author_name = AUTHOR_NAME,
                               featured = True if featured else False,
                               body = body  )
            
            post.put()
            counter.increment("Posts_Count")
            deferred.defer(worker.deferred_update_last_sitemap,post.key())
            deferred.defer(worker.deferred_update_tags_counter,tags)
            deferred.defer(worker.deferred_update_category_counter,category)
            result[action] = "Done"

        elif action =='editpost_init':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity = models.Post.get(post_id)
                if entity:
                    return render_template(False, 
                                            result, 
                                            action, 
                                            title = entity.title,
                                            link = entity.link,
                                            description = entity.description,
                                            tags = entity.tags,
                                            category = entity.category,
                                            img_path = entity.get_image_path(),
                                            body = entity.body,
                                            post_id = post_id,
                                            featured = entity.featured
                                            )
                else:
                    result[action] = "Post Id Not found"
                    submitted = False
            else:
                result[action] = "Post Id is required"
                submitted = False
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
                
                #Various checks
                if not title:
                    result[action] = "Please fill in all required fields (*)"
                    submitted = False
                if link and not utils.link_is_valid(link):
                    result[action] = "Link is not valid"
                    submitted = False
                if thumbnail and thumbnail_url:
                    result[action] = "Only one kind of img is allowed"
                    submitted = False
                if thumbnail_url and not utils.link_is_valid(thumbnail_url):
                    result[action] = "url_img is not a valid URL"
                    submitted = False
                if not submitted:
                    return render_template(submitted, 
                                           result, 
                                           action, 
                                           title = title,
                                           link = link,
                                           description = description,
                                           tags = tags.split(),
                                           category = category,
                                           body = body,
                                           url_img = thumbnail_url,
                                           featured = featured
                                           )
                
                if thumbnail_url:
                    response = urlfetch.fetch(url=thumbnail_url,
                                   method=urlfetch.GET,
                                   deadline = 10)
                    thumbnail = response.content
                if thumbnail:
                    thumbnail = images.resize(thumbnail, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)
                    thumbnail_for_db= db.Blob(thumbnail)
                else:
                    thumbnail_for_db= None
                
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
                if thumbnail_for_db:
                    entity_post.thumbnail = thumbnail_for_db
                if delete_img:
                    entity_post.thumbnail = None            
                entity_post.put()
                worker.deferred_update_tags_counter(entity_post.tags, tags_old)
                worker.deferred_update_category_counter(entity_post.category, category_old)
                result[action] = "Done"
        elif action =='deletepost':
            post_id = web.input(post_id = None)['post_id']
            if post_id:
                entity = models.Post.get(post_id)
                if entity:
                    entity.delete()
                    counter.decrement("Posts_Count")
                    worker.deferred_update_tags_counter([],entity.tags)
                    worker.deferred_update_category_counter(None, entity.category)
                    result[action] = "Done"
                else:
                    result[action] = "Post ID not found"
                    submitted = False
            else:
                result[action] = "Post ID is required"
                submitted = False
        
        #Default
        return render_template(submitted, 
                               result, 
                               action
                              )

        
class Warmup:
    """
    Warming Requests for avoiding latency
    """
    def GET(self):
        pass