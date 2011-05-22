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
            

            
