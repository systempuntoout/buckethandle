"""
 Routes to controllers
"""

urls = (
  '/tag/(.*)', 'app.controllers.main.Tags',
  '/tagcloud','app.controllers.main.TagCloud',
  '/post', 'app.controllers.main.Post',
  '/post/(\d+)/.*', 'app.controllers.main.Post',
  '/about', 'app.controllers.main.About',
  '/img', 'app.controllers.main.Image',
  '/ajax/tags','app.controllers.ajax.Tags',
  '/admin','app.controllers.admin.Admin',
  '/index.xml', 'app.controllers.main.Feed',
  '/feed/index.rss', 'app.controllers.main.Feed',
  '/_ah/warmup','app.controllers.admin.Warmup',
  '/.*', 'app.controllers.main.Index',
)