"""
 Routes to controllers
"""

urls = (
  '/tag', 'app.controllers.main.Tags',
  '/tag/(.*)', 'app.controllers.main.Tags',
  '/featured', 'app.controllers.main.Featured',
  '/tagcloud','app.controllers.main.TagCloud',
  '/submit','app.controllers.main.Submit',
  '/post', 'app.controllers.main.Post',
  '/post/([\w_-]+)(?:/([\w-]+))?/?', 'app.controllers.main.Post',
  '/about', 'app.controllers.main.About',
  '/search', 'app.controllers.main.Search',
  '/img/([\w_-]+)(?:/.*)?', 'app.controllers.main.Image',
  '/ajax/tags','app.controllers.ajax.Tags',
  '/ajax/links','app.controllers.ajax.Links',
  '/admin','app.controllers.admin.Admin',
  '/admin/content','app.controllers.admin.ContentDiscoverer',
  '/index.xml', 'app.controllers.main.Feed',
  '/cse.xml', 'app.controllers.main.Cse',
  '/sitemap.xml', 'app.controllers.main.Sitemap',
  '/sitemap_(\d+).xml', 'app.controllers.main.Sitemap',
  '/sitemap_index.xml', 'app.controllers.main.SitemapIndex',
  '/robots.txt', 'app.controllers.main.Robots',
  '/feed/index.rss', 'app.controllers.main.Feed',
  '/_ah/warmup','app.controllers.admin.Warmup',
  '/', 'app.controllers.main.Index',
)

"""
 Routes for sitemap
"""

sitemap_urls = ('/',
                '/tag',
                '/post',
                '/featured',
                '/about')
