from google.appengine.api import memcache
from app.config.settings import GENERIC_ERROR, NOT_FOUND_ERROR
import logging, web
import app.db.models as models
from google.appengine.ext import ereporter
import app.utility.utils as utils
from app.utility.utils import cachepage

ereporter.register_logger()

render = web.render
            
class Tags:
    """
    Return tags for auto completion
    """
    @cachepage()
    def GET(self):
        web.header('Content-type', 'text/plain')
        try:
            tag_filter = web.input()['q']
            return models.Tag.get_tags_by_filter(tag_filter) 
        except Exception, exception:
            return ""

class Markdown:
    """
    Return markdown data for Markitup preview
    """
    def POST(self):
        data = web.input(data = None)['data']
        return render.admin.markdown_preview(data)
            
class Links:
    """
    Check if a given link is already stored
    """
    def GET(self):
        web.header('Content-type', 'application/json')
        link = web.input(check = None)['check']
        if link and utils.link_is_valid(link):
            link_is_stored = models.Post.get_post_by_link(link.strip())
            if not link_is_stored: 
                if link.strip().endswith('/'):
                    link_is_stored = models.Post.get_post_by_link(link.strip()[:-1]) #check without slash
                else:
                    link_is_stored = models.Post.get_post_by_link("%s%s" % (link.strip(), '/')) #check with slash
            if link_is_stored:    
                return '{"result":"[ The link is known ]","clazz":"message_KO"}' 
            else:
                return '{"result":"[ This link looks new ]","clazz":"message_OK"}'    
        else:
            return '{"result":"","clazz":""}'
            
