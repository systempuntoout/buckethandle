import web
i18ns = web.i18ns

"""
 Routes to controllers
"""

urls = (
  '/tag', 'app.controllers.main.Tags',
  '/tag/(.*)', 'app.controllers.main.Tags',
  '/%s' % i18ns['ROUTE_FEATURED'], 'app.controllers.main.Featured',
  '/%s' % i18ns['ROUTE_TAGCLOUD'],'app.controllers.main.TagCloud',
  '/submit','app.controllers.main.Submit',
  '/%s' % i18ns['ROUTE_POST'], 'app.controllers.main.Post',
  '/%s/([\w_-]+)(?:/([\w-]+))?/?' % i18ns['ROUTE_POST'], 'app.controllers.main.Post',
  '/%s' % i18ns['ROUTE_ABOUT'], 'app.controllers.main.About',
  '/%s' % i18ns['ROUTE_PRIVACY'], 'app.controllers.main.Privacy',
  '/%s' % i18ns['ROUTE_SEARCH'], 'app.controllers.main.Search',
  '/img/([\w_-]+)(?:/.*)?', 'app.controllers.main.Image',
  '/ajax/tags','app.controllers.ajax.Tags',
  '/ajax/links','app.controllers.ajax.Links',
  '/ajax/markdown','app.controllers.ajax.Markdown',
  '/admin/tags','app.controllers.admin.Tags',
  '/admin','app.controllers.admin.Admin',
  '/admin/content','app.controllers.admin.ContentDiscoverer',
  '/admin/tags','app.controllers.admin.Tags',
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
                '/%s' % i18ns['ROUTE_POST'],
                '/featured',
                '/%s' % i18ns['ROUTE_ABOUT'])
