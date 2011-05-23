from google.appengine.ext import db
from app.utility.utils import memcached
from app.config.settings import *
import app.utility.utils as utils
import logging

class Post(db.Model):
    title = db.StringProperty(required = True)
    link = db.LinkProperty(required = True)
    description = db.StringProperty(required = True)
    tags = db.ListProperty(str)
    category = db.StringProperty(choices = CATEGORIES)
    body = db.TextProperty()
    slug = db.StringProperty()
    thumbnail = db.BlobProperty()
    author_name = db.StringProperty()
    featured = db.BooleanProperty(default = False)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)
    created = db.DateTimeProperty(required = True, auto_now_add = True)
    
    @staticmethod
    @memcached('get_posts_count', 3600, lambda tags_filter = [], category_filter= '': "%s_%s" % ('.'.join(sorted(tags_filter)), category_filter))
    def get_posts_count(tags_filter = [], category_filter = ''):
        posts =  Post.all(keys_only = True)
        if category_filter:
            posts.filter('category', category_filter )
        for tag in tags_filter:
          if tag:
              posts.filter('tags', tag)
        return posts.count(limit = None)

    @staticmethod
    @memcached('get_posts', 3600, lambda limit, offset, tags_filter  = [], category_filter = '': "%s_%s_%s_%s" % (limit,offset,'.'.join(sorted(tags_filter)), category_filter))
    def get_posts(limit, offset, tags_filter = [], category_filter = ''):
        posts =  Post.all()
        if category_filter:
            posts.filter('category', category_filter )
        for tag in tags_filter:
          if tag:
              posts.filter('tags', tag)
        return posts.fetch(limit = limit, offset = offset)
    
    @staticmethod
    @memcached('get_recent_posts', 3600*24)
    def get_recent_posts():
        posts =  Post.all().fetch(RECENT_POST_NUM)
        return posts
    
    @staticmethod
    @memcached('get_post', 3600*24, lambda post_id: post_id)
    def get_post(post_id):
        return Post.get_by_id(post_id)
        
    def get_image_path(self):
        if self.thumbnail is not None:
            return "/img?id=%s" % self.key().id()
        else:
            return utils.get_predefined_image_link(self.link, self.category)
    
    def get_path(self):
        return "%s/%s" % (self.key().id(), self.slug)
            
    @staticmethod
    @memcached('get_prev_next', 3600*24, lambda post: post.key().id())
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
    @memcached('get_tags', 3600, lambda limit = NO_LIMIT : limit )
    def get_tags(limit = NO_LIMIT ):
        tags =  Tag.all().filter('counter > ', 0).order('-counter')

        return tags.fetch(limit = limit)
        
        
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
    @memcached('get_categories', 3600, lambda limit = NO_LIMIT : limit )
    def get_categories(limit = NO_LIMIT ):
        category =  Category.all().filter('counter > ', 0)

        return category.fetch(limit = limit)