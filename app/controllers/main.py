import os
import logging
import re

from google.appengine.api import memcache
from google.appengine.ext import ereporter
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.db import BadKeyError

import web
from app.config.settings import *
from app.config.urls import sitemap_urls
import app.db.models as models
import app.utility.utils as utils
from app.utility.utils import cachepage

ereporter.register_logger()

render = web.render 
i18ns = web.i18ns

def render_template(content, **kwargs):
    """
     Renders the layout template with the content page and the dynamic navbar values
    """
    posts_total_count = models.Post.get_posts_count()  
    tag_cloud = models.Tag.get_tags(limit = NAVBAR_CLOUDSIZE)
    categories = models.Category.get_categories()
    return render.layout(content, 
                         tag_cloud = tag_cloud, 
                         posts_total_count = posts_total_count, 
                         categories = categories, 
                         user = users.get_current_user(),
                         is_user_admin = users.is_current_user_admin() ,
                         login_url = users.create_login_url("/"),
                         logout_url = users.create_logout_url("/"),
                          **kwargs)

def render_error(error, **kwargs):
    """
     Renders the error page
    """
    return render.layout(render.oops(error), title = i18ns['TITLE_ERROR'], navbar = False)

    
class Index:
    """
    Homepage
    """
    def GET(self):
        page = int(web.input(page = 1)['page'])
        category = web.input(category = '')['category']
        
        posts_count = models.Post.get_posts_count(category_filter= category)
        posts = models.Post.get_posts(page, limit = POSTS_PER_PAGE, offset = POSTS_PER_PAGE * (page - 1), category_filter= category)
        
        return render_template(render.index(posts, 
                                            selected_category = category, 
                                            pagination = utils.Pagination(posts_count, page, POSTS_PER_PAGE),
                                            is_user_admin = users.is_current_user_admin()),
                                            title = "%s" % (category if category else i18ns['TITLE_HOME']))


class Post:
    """
    Post
    """
    def GET(self, post_id = None, slug = None):
        try:
            #Return to canonical if the slug is missing
            if post_id and not slug:
                post = models.Post.get(post_id)
                if post:
                    return web.seeother('/%s/%s/%s' % (i18ns['ROUTE_POST'], post_id, post.slug))
                else:
                    raise web.notfound()
            #Get post 
            if post_id:            
                post = models.Post.get_post(post_id)
            else:
                post = models.Post.get_latest_post()
        
            if post:
                #Return to canonical if the slug is truncated
                if slug and slug.strip() != post.slug:
                    return web.seeother('/%s/%s/%s' % (i18ns['ROUTE_POST'],post_id, post.slug))
                    
                prev_post, next_post = models.Post.get_prev_next(post)
            else:
                raise web.notfound()
        
            return render_template(render.post(post, 
                                               prev_post, 
                                               next_post, 
                                               utils.ContentDiscoverer(post.link, post.category).get_content_block(),
                                               is_user_admin = users.is_current_user_admin()), 
                                               title = post.title,
                                               canonical = "%s/%s" % (i18ns['ROUTE_POST'],post.get_path()),
                                               meta_description = utils.get_metadescription(post))
        except BadKeyError:
                raise web.notfound()

class Tags:
    """
    Tags
    """
    def POST(self, tags):
        return self.GET(tags)
        
    def GET(self, tags = None):
        if tags:
            tags = [tag.lower() for tag in tags.split('/')]
        else: 
            tags = []
            
        add_tag = web.input(addtag = None)['addtag']
        remove_tag = web.input(removetag = None)['removetag']
        page = int(web.input(page = 1)['page'])
        category = web.input(category = '')['category']
        
        if add_tag in tags  or len(tags)>= MAX_NUMBER_OF_TAGS_FILTERS:
            add_tag = None
        
        if add_tag:
            tags = tags + [tag.lower() for tag in add_tag.split()]
            if category:
                return web.seeother('/tag/%s?category=%s' % (web.urlquote('/'.join(tags)), category))
            else:
                return web.redirect('/tag/%s' % web.urlquote('/'.join(tags)))
        if remove_tag:
            tags.remove(remove_tag.lower())
            if category:
                return web.seeother('/tag/%s?category=%s' % (web.urlquote('/'.join(tags)), category))
            else:
                return web.seeother('/tag/%s' % web.urlquote('/'.join(tags)))
        
        posts_count = models.Post.get_posts_count(tags_filter = tags, category_filter= category)
        posts = models.Post.get_posts(page, limit = POSTS_PER_PAGE, offset = POSTS_PER_PAGE * (page - 1), tags_filter = tags, category_filter= category)
        
        return render_template(render.index(posts, 
                                            tags, 
                                            category, 
                                            pagination = utils.Pagination(posts_count, page, POSTS_PER_PAGE),
                                            is_user_admin = users.is_current_user_admin()),
                                            title = "%s %s" % (category if category else '',' '.join(tags) if tags else (i18ns['TITLE_POST'] if not category else '')))
        

class TagCloud:
    """
    Tag Cloud
    """
    @cachepage()
    def GET(self):
        show_all = web.input(showall = False)['showall']
        if show_all:
            tag_cloud = models.Tag.get_tags()
        else:
            tag_cloud = models.Tag.get_tags(MAIN_CLOUDSIZE)
        return render_template(render.tagcloud(tag_cloud, show_all),
                               title = i18ns['TITLE_TAGCLOUD'],
                               meta_description = i18ns['META_TAGCLOUD'])

class Featured:
   """
   Featured
   """
   def GET(self):
       featured_posts = models.Post.get_featured_posts()

       return render_template(render.featured(featured_posts, is_user_admin = users.is_current_user_admin()),
                              title = i18ns['TITLE_FEATURED'])
class About:
    """
    About
    """
    @cachepage()
    def GET(self):
        return render_template(render.about(), title = i18ns['TITLE_ABOUT'])

class Search:
    """
    Search
    """
    def GET(self):
        return render_template(render.search(), title = i18ns['TITLE_SEARCH'])

class Feed:
     """
     Feed
     """
     def GET(self):
         if FEED_PROXY and not os.environ.get('HTTP_USER_AGENT').startswith(FEED_PROXY_USER_AGENT):
            web.redirect(FEED_PROXY)
         else:
             posts = models.Post.get_recent_posts()
             web.header('Content-type', 'application/atom+xml')
             return render.feed(posts, utils.now().strftime("%Y-%m-%dT%H:%M:%SZ") )

class Cse:
     """
     Google Cse for Search
     """
     def GET(self):
         web.header('Content-type', 'text/xml')
         return render.cse()

class Sitemap:
      """
      Sitemap
      """
      def GET(self, id = None):
          web.header('Content-type', 'text/xml')
          if id:
             return models.Sitemap.get_sitemap_by_id(int(id))
          else:
              return render.sitemap(sitemap_urls)

class SitemapIndex:
    """
    Sitemap Index
    """
    def GET(self):
        web.header('Content-type', 'text/xml')
        sitemaps = models.Sitemap.get_sitemaps() 
        return render.sitemap_index(sitemaps)

class Robots:
       """
       Robots
       """
       def GET(self):
           disallow_all = False
           if REDIRECT_FROM_APPENGINE_HOST_TO_HOST and os.environ.get('HTTP_HOST').endswith(APPENGINE_HOST):
                disallow_all = True
           return render.robots(disallow_all)          
          
                             
class Image:
     """
     Image
     """
     def GET(self, post_id):
         try:
             post = models.Post.get_post(post_id)

             if post and post.thumbnail:
                 web.header('Content-type', 'image/png')
                 web.header('Cache-Control','public, max-age=86400')
                 return post.thumbnail
             else:
                 raise web.notfound()
         except:
             raise web.notfound()


class Submit:
     """
     Submit
     """
     def POST(self):
         return self.GET()

     def GET(self):
         result = {}
         posts = []
         tags_filter = []
         action = web.input(action = None)['action']
        
         if action =='submit_init':
             title = web.input(title = '')['title']
             link = web.input(link = '')['link']
             description = web.input(description = '')['description']
             tags = web.input(tags = '')['tags']
             base_link = utils.get_base_link(link)
             if base_link in AUTO_CONTENT_BY_LINK:
                 if 'category' in AUTO_CONTENT_BY_LINK[base_link]:
                     selected_category = AUTO_CONTENT_BY_LINK[base_link]['category']
                 else:
                     selected_category = ''
             else: 
                 selected_category = ''

             tags = list(set(tags.split()) - set(TAGS_BLACK_LIST))
             return render_template(render.submit(False, '', title, link, description, tags, selected_category),
                                  title = 'Posts')
         elif action =='submit':
             title = web.input(title = None)['title']
             link = web.input(link = None)['link']
             description = web.input(description = None)['description']
             tags = web.input(tags = None)['tags']
             category = web.input(category = None)['category']
             
             if title.strip() and link.strip() and tags.strip():
                 mail.send_mail(sender="%s <%s>" % (CMS_NAME, MAIL_ADMIN),
                               to="Admin <%s>" % MAIL_ADMIN,
                               subject="%s - Link submitted %s" % (CMS_NAME, utils.now().strftime("%Y-%m-%d %H:%M:%S")),
                               body="""
                 Link submission:

                 Title: %s
                 Link: %s
                 Description: %s
                 Tags: %s
                 Category: %s
                 User: %s
                 """ % (title, link, description, tags, category, users.get_current_user()))
                 title = link = description = tags = ""
                 submitted = True
                 message = "Thanks for your submission, we'll review it soon."
             else:
                 submitted = False
                 message = "Please fill in all required fields (*)"
             return render_template(render.submit(submitted, message, title, link , description, tags, category),
                                   title = 'Posts')
         else:
            return None

