from google.appengine.api import memcache
from app.config.settings import GENERIC_ERROR, NOT_FOUND_ERROR
import logging, web
import app.db.models as models
from google.appengine.ext import ereporter

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
        if link:
            link_is_stored = models.Post.get_post_by_link(link.trim())
            if link_is_stored:    
                return '{"result":"[Link is already there]","clazz":"link_KO"}' 
            else:
                return '{"result":"[Link looks ok]","clazz":"link_OK"}'    
        else:
            return '{"result":"","clazz":""}'
            
