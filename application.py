"""
    BucketHandle: lightweight cms to tag and collect knowledge
"""
import os
import logging
import webob, urlparse

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

import web
import app.utility.utils as utils
import app.config.settings as settings
from app.config.settings import *

web.i18ns = utils.get_i18ns(DEFAULT_LANGUAGE)

global_template = {
            'safemarkdown':web.safemarkdown,
            'commify': web.utils.commify,
            'urlquote':web.net.urlquote,
            'htmlquote':web.net.htmlquote,
            'settings': settings,
            'utils': utils,
            'i18ns': web.i18ns,
            'development' : os.environ['SERVER_SOFTWARE'].startswith('Dev')
          }

web.render = render = web.template.render('app/views/', globals = global_template, cache = True)


                                               
def notfound():
    return web.notfound(render.layout(render.oops(web.i18ns['PAGE_NOT_FOUND_ERROR']), title ='Error', navbar = False, is_user_admin = users.is_current_user_admin()))
def internalerror():
    return web.internalerror(render.layout(render.oops(web.i18ns['SERVER_ERROR']), title ='Error', navbar = False, is_user_admin = users.is_current_user_admin()))

from app.config.urls import urls

def redirect_from_appspot(wsgi_app):
    """Handle redirect to my domain if called from appspot (and not SSL)"""
    from_server = APPENGINE_HOST
    to_server = HOST

    def redirect_if_needed(env, start_response):
        if REDIRECT_FROM_APPENGINE_HOST_TO_HOST and env["HTTP_HOST"].endswith(from_server) and env.get("HTTPS") == "off":
            # Parse the URL
            request = webob.Request(env)
            scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
            url = urlparse.urlunsplit([scheme, to_server, path, query, fragment])
            if not path.startswith('/admin') and not path.startswith('/robots.txt'):
                start_response("301 Moved Permanently", [("Location", url)])
                return ["301 Moved Peramanently", "Click Here %s" % url]
        return wsgi_app(env, start_response)
    return redirect_if_needed

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
app = app.wsgifunc() 
logging.getLogger().setLevel(logging.ERROR)
app = redirect_from_appspot(app)

