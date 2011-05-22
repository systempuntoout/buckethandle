from google.appengine.ext import db
from app.utility.utils import memcached
from app.config.settings import *
import app.utility.utils as utils

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
    def update_tag(name, removed = False):
        tag = Tag.get_by_key_name(name)
        if tag:
            if removed:
                tag.counter -= 1
                if tag.counter == 0:
                    tag.delete()
            else:
                tag.counter += 1
                tag.put()

        else:
            if not removed:
                Tag(name = name, key_name = name, counter = 1).put()

    @staticmethod
    @memcached('get_tags', 3600, lambda limit = NO_LIMIT : limit )
    def get_tags(limit = NO_LIMIT ):
        tags =  Tag.all().order('-counter')

        return tags.fetch(limit = limit)
        
        
class Category(db.Model):
    name = db.StringProperty(required = True)
    counter = db.IntegerProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)

    @staticmethod
    def update_category(name, removed = False):
        category = Category.get_by_key_name(name)
        if category:
            if removed:
                category.counter -= 1
                if category.counter == 0:
                    category.delete()
            else:
                category.counter += 1
                category.put()

        else:
            if not removed:
                Category(name = name, key_name = name, counter = 1).put()

    @staticmethod
    @memcached('get_categories', 3600, lambda limit = NO_LIMIT : limit )
    def get_categories(limit = NO_LIMIT ):
        category =  Category.all()

        return category.fetch(limit = limit)