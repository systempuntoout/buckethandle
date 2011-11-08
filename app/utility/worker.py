import logging
import app.db.models as models
import app.utility.utils as utils
from google.appengine.api import memcache

def deferred_update_last_sitemap(post_key):
    models.Sitemap.update_last_sitemap(post_key)

def deferred_delete_post_sitemap(post_key):
    for sitemap in models.Sitemap.all():
        if post_key in sitemap.post_keys:
            sitemap.post_keys = [x for x in sitemap.post_keys if x != post_key]
            sitemap.post_count -= 1
            sitemap.put()

def deferred_ping_sitemap():
    utils.ping_googlesitemap()
    
def deferred_cache_tags():
    models.Tag.cache_tags()

def deferred_update_tags_counter(tags_new , tags_old = []):
    models.Tag.update_tags(tags_new, tags_old)

def deferred_update_category_counter(category_new, category_old = None ):
    models.Category.update_category(category_new, category_old)
    
def deferred_flush_cache_light():
    memcache.delete('get_posts:10_0__') #Delete first page cached posts
    memcache.delete('get_recent_posts') #Delete recent posts used for generating feed
    