from google.appengine.api import memcache
from app.config.settings import GENERIC_ERROR, NOT_FOUND_ERROR
import logging, web
import app.db.models as models
from google.appengine.ext import ereporter
import urlparse

ereporter.register_logger()

            
class Tags:
    """
    Return tags for auto completion
    """
    def GET(self):
        web.header('Content-type', 'text/plain')
        try:
            tag_filter = web.input()['q']
            tags = models.Tag.get_tags() 
            return '\n'.join([tag.name for tag in tags if tag.name.startswith(tag_filter)])
        except Exception, exception:
            return ""
            
class Links:
    """
    Check if a given link is already stored
    """
    def GET(self):
        web.header('Content-type', 'application/json')
        link = web.input(check = None)['check']
        if link and (link.startswith('http://') or link.startswith('https://')):
            link_is_stored = models.Post.get_post_by_link(link.strip())
            if link_is_stored:    
                return '{"result":"[ We already know this link ]","clazz":"message_KO"}' 
            else:
                return '{"result":"[ This link looks new ]","clazz":"message_OK"}'    
        else:
            return '{"result":"","clazz":""}'
            
