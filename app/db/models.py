import logging
import string
import datetime
import itertools

from google.appengine.ext import db
from google.appengine.api import memcache

import web
import app.utility.utils as utils
import app.db.counter as counter
from app.utility.utils import memcached
from app.config.settings import *


render = web.render 

class Post(db.Model):
    title = db.StringProperty(required = True)
    link = db.LinkProperty()
    description = db.StringProperty()
    tags = db.ListProperty(str, required = True)
    category = db.StringProperty(choices = CATEGORIES)
    body = db.TextProperty()
    slug = db.StringProperty()
    thumbnail = db.BlobProperty()
    author_name = db.StringProperty()
    featured = db.BooleanProperty(default = False)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)
    created = db.DateTimeProperty(required = True, auto_now_add = True)
    
    @staticmethod
    @memcached('get_posts_count', 3600*24, lambda tags_filter = [], category_filter= '': "%s_%s" % ('.'.join(sorted(tags_filter)), category_filter))
    def get_posts_count(tags_filter = [], category_filter = ''):
        #Use the sharded counter for the unfiltered number of posts count
        if not tags_filter and not category_filter:
            return counter.get_count("Posts_Count")
        
        #Use the counter of the tag
        if len(tags_filter) == 1 and not category_filter:
            tag = Tag.get_tag(tags_filter[0])
            if tag:
                return tag.counter
            else:
                return 0
        #Use the counter of the category
        if category_filter and not tags_filter:
            category = Category.get_category(category_filter)
            if category:
                return category.counter
            else:
                return 0    
        posts =  Post.all(keys_only = True)
        if category_filter:
            posts.filter('category', category_filter )
        for tag in tags_filter:
          if tag:
              posts.filter('tags', tag)
        return posts.count(limit = None)

    @staticmethod
    @memcached('get_posts', 3600*24, lambda page, limit, offset, tags_filter  = [], category_filter = '': "%s_%s_%s_%s" % (limit,offset,'.'.join(sorted(tags_filter)), category_filter))
    def get_posts(page, limit, offset, tags_filter = [], category_filter = ''):
        posts =  Post.all()
        if category_filter:
            posts.filter('category', category_filter )
        for tag in tags_filter:
          if tag:
              posts.filter('tags', tag)
        bookmark = memcache.get("%s:%s_%s_%s" % ('get_posts_cursor', page-1,'.'.join(sorted(tags_filter)), category_filter))
        if bookmark:
            posts.with_cursor(start_cursor = bookmark)
            fetched_post = posts.fetch(limit = limit)
            memcache.set("%s:%s_%s_%s" % ('get_posts_cursor', page,'.'.join(sorted(tags_filter)), category_filter), posts.cursor())
        else:
            if offset ==  0:
                fetched_post = posts.fetch(limit = limit) 
                memcache.set("%s:%s_%s_%s" % ('get_posts_cursor', page,'.'.join(sorted(tags_filter)), category_filter), posts.cursor())
            else:
                #Offset consumes a lot of Datastore reads, without bookmark I return nothing
                fetched_post = []
            
        
        return fetched_post
    
    @staticmethod
    @memcached('get_recent_posts', 3600*24)
    def get_recent_posts():
        posts =  Post.all().order("-created").fetch(RECENT_POST_NUM)
        return posts
    
    @staticmethod
    @memcached('get_featured_posts', 3600*24)
    def get_featured_posts():
        posts =  Post.all().order("-created").filter('featured =', True).fetch(FEATURED_POST_NUM)
        return posts
    
    @staticmethod
    @memcached('get_post', 3600*24, lambda post_id: post_id)
    def get_post(post_id):
        return Post.get(post_id)
        
    def get_image_path(self):
        if self.thumbnail is not None:
            return "/img/%s/%s.png" % (self.key(), self.slug)
        else:
            return utils.get_predefined_image_link(self.link, self.category)
    
    def get_path(self):
        return "%s/%s" % (self.key(), self.slug)
            
    @staticmethod
    @memcached('get_prev_next', 3600*24, lambda post: post.key())
    def get_prev_next(post):
      """Chronologically previous and next post for the passed post"""

      posts =  Post.all().order('-created')
      posts.filter('created <', post.created)
      prev_post = posts.get()

      posts =  Post.all().order('created')
      posts.filter('created >', post.created)
      next_post = posts.get()

      return prev_post, next_post   

    @staticmethod
    @memcached('get_latest_post', 3600*24)
    def get_latest_post():
      post =  Post.all().order('-created').get()
      return post   
      
    @staticmethod
    @memcached('get_post_by_link', 3600, lambda link: link)
    def get_post_by_link(link):
      return Post.all().filter('link =', link).get()
              
        
class Tag(db.Model):
    name = db.StringProperty(required = True)
    counter = db.IntegerProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)

    @staticmethod
    def update_tags(tags_new, tags_old):
        tags_to_update = []
        tag_to_increment = set(tags_new) - set(tags_old)
        for tag in tag_to_increment:
            tag_entity = Tag.get_by_key_name(tag)
            if tag_entity:
                tag_entity.counter +=1
            else:
                tag_entity = Tag(key_name= tag, name = tag, counter = 1)   
            tags_to_update.append(tag_entity)

        tag_to_decrement =  set(tags_old) - set(tags_new)
        for tag in tag_to_decrement:
            tag_entity = Tag.get_by_key_name(tag)
            if tag_entity and tag_entity.counter > 0:
                tag_entity.counter -=1       
                tags_to_update.append(tag_entity)      
        db.put(tags_to_update)

    @staticmethod
    @memcached('get_tags', 3600*24, lambda limit = NO_LIMIT, tag_filter = None : '%s_%s' % (limit, tag_filter) )
    def get_tags(limit = NO_LIMIT, tag_filter = None ):
        tags =  Tag.all()
        if tag_filter:
            tags = tags.filter('name >=', tag_filter).filter('name <', tag_filter + u'\ufffd')
            tags.fetch(limit = limit)
            tags = sorted(tags, key=lambda x: x.counter, reverse=True)
            return tags
        else:
            tags = tags.filter('counter >', 0).order('-counter')
            return tags.fetch(limit = limit)
    
    @staticmethod
    @memcached('get_tag', 3600*24, lambda name: name)
    def get_tag(name):
        return Tag.all().filter('name =', name).get()    
    
    @staticmethod
    @memcached('get_tags_by_filter', 3600*24*20, lambda tag_filter : tag_filter )
    def get_tags_by_filter(tag_filter):
        tags = Tag.get_tags(limit = 20, tag_filter = tag_filter) 
        return '\n'.join([tag.name for tag in tags])
        
    @staticmethod
    def cache_tags():
        for letter in string.ascii_lowercase:
            Tag.get_tags_by_filter(letter)
        return True 
class Category(db.Model):
    name = db.StringProperty(required = True)
    counter = db.IntegerProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)

    @staticmethod
    def update_category(category_new, category_old):
        if category_new != category_old:
            if category_new:
                category_entity = Category.get_by_key_name(category_new)
                if category_entity:
                    category_entity.counter +=1
                else:
                    category_entity = Category(key_name= category_new, name = category_new, counter = 1)
                category_entity.put()
            if category_old:
                category_entity = Category.get_by_key_name(category_old)
                if category_entity and category_entity.counter > 0:
                   category_entity.counter -=1
                   category_entity.put()

    @staticmethod
    @memcached('get_categories', 3600*24, lambda limit = NO_LIMIT : limit )
    def get_categories(limit = NO_LIMIT ):
        category =  Category.all().filter('counter > ', 0).order('-counter')
        return category.fetch(limit = limit)
        
    @staticmethod
    @memcached('get_category', 3600*24, lambda name: name)
    def get_category(name):
        return Category.all().filter('name =', name).get()
        
class Sitemap(db.Model):
    post_count = db.IntegerProperty(default = 0)
    post_keys = db.StringListProperty(default = [])    
    content = db.TextProperty(default ='')
    archived = db.BooleanProperty(default = False)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    @staticmethod
    def get_last_sitemap():
        entity = Sitemap.all().order('-created').get()
        if entity:
            if entity.post_count >= POSTS_PER_SITEMAP:
                entity.content = unicode(render.sitemap_posts(entity.post_keys))
                entity.archived = True
                entity.put()
                entity = Sitemap()
                entity.put()
        else:
            entity = Sitemap()
            entity.put()
        return entity
        
    @staticmethod
    def update_last_sitemap(key):
        last_sitemap = Sitemap.get_last_sitemap()
        last_sitemap.post_count += 1
        last_sitemap.post_keys.insert(0, str(key))
        last_sitemap.put()
    
    
    @staticmethod
    def get_sitemaps():
        sitemaps = Sitemap.all().order('-created').fetch(500)
        return sitemaps
        
    @staticmethod
    @memcached('get_sitemap_by_id', 3600*24, lambda id : int(id) )
    def get_sitemap_by_id(id):
        entity = Sitemap.get_by_id(id)
        if entity:
            if entity.content:
                return entity.content
            else:
                posts = Post.get(entity.post_keys)
                return unicode(render.sitemap_posts(posts))
        else:
            raise web.notfound()

class Feed(db.Model):
    name = db.StringProperty(required = True)
    link = db.LinkProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)
    created = db.DateTimeProperty(required = True, auto_now_add = True)
    
    @staticmethod
    def get_feeds():
        feeds = Feed.all().order('-created').fetch(500)
        return feeds
        
class FeedEntry(db.Model):
    title = db.StringProperty(required = True)
    link = db.LinkProperty(required = True)
    tags = db.ListProperty(str, required = True)
    reviewed = db.BooleanProperty(required = True, default = False)
    feed = db.ReferenceProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)
    created = db.DateTimeProperty(required = True, auto_now_add = True)

    @staticmethod
    def get_posts():
        posts = FeedEntry.all().filter('reviewed =', False).order('-created').fetch(500)
        return posts

    @staticmethod
    def check_for_new_posts():
        post = FeedEntry.all().filter('reviewed =', False).filter('created >=', datetime.date.today() - datetime.timedelta(1)).get()
        return post