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
        elif action =='create':
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
            
            post = models.Post(title = title,
                               link = db.Link(link),
                               description = description,
                               tags = tags,
                               category = category,
                               thumbnail = blob_thumbnail,
                               slug = utils.slugify(title),
                               author_name = users.get_current_user().nickname(),
                               body = body  )
            
            result['create'] = post.put()
            worker.deferred_update_tags_counter(tags)
            worker.deferred_update_category_counter(category)
            
            
        posts = models.Post.all()
        for tag in tags_filter:
          posts.filter('tags', tag)
        
        return render.layout(render.admin(result, posts), title ='Admin', navbar = False, admin = users.get_current_user())

        
class Warmup:
    """
    Warming Requests for avoiding latency
    """
    def GET(self):
        pass