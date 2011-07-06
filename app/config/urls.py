"""
 Routes to controllers
"""

urls = (
  '/tag/(.*)', 'app.controllers.main.Tags',
  '/featured', 'app.controllers.main.Featured',
  '/tagcloud','app.controllers.main.TagCloud',
  '/submit','app.controllers.main.Submit',
  '/post', 'app.controllers.main.Post',
  '/post/(\w+)/.*', 'app.controllers.main.Post',
  '/about', 'app.controllers.main.About',
  '/search', 'app.controllers.main.Search',
  '/img', 'app.controllers.main.Image',
  '/ajax/tags','app.controllers.ajax.Tags',
  '/ajax/links','app.controllers.ajax.Links',
  '/admin','app.controllers.admin.Admin',
  '/index.xml', 'app.controllers.main.Feed',
  '/cse.xml', 'app.controllers.main.Cse',
  '/sitemap.xml', 'app.controllers.main.Sitemap',
  '/feed/index.rss', 'app.controllers.main.Feed',
  '/_ah/warmup','app.controllers.admin.Warmup',
  '/.*', 'app.controllers.main.Index',
)

"""
 Routes for sitemap
"""

sitemap_urls = ('/',
                '/tag',
                '/post',
                '/tagcloud',
                '/featured',
                '/about')
