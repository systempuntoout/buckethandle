from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def about():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<div>\n'])
    extend_([u'  <p>\n'])
    extend_([u'   ', escape_(safemarkdown(settings.ABOUT), False), u'  \n'])
    extend_([u'  </p>\n'])
    extend_([u'</div>                                 \n'])

    return self

about = CompiledTemplate(about, 'app/views/about.html')
join_ = about._join; escape_ = about._escape

# coding: utf-8
def admin (result, title = '', link = '', description = '', tags = [], category = '', img_path ='', body = '', post_id =''):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' <div>\n'])
    extend_([u'     <p>ADMIN CONSOLE</p>\n'])
    extend_([u'     <ul>\n'])
    extend_([u'           <li><a href="/admin?action=memcachestats">Memcache stats </a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcacheflush">Memcache flush </a></li>\n'])
    extend_([u'     </ul>\n'])
    extend_([u'     <p><b>Result:</b></p>\n'])
    for key in loop.setup(result.keys()):
        extend_(['      ', u'* ', escape_(("%s - %s" % (key, result[key])), True), u'<br>\n'])
    extend_([u'     <ul>\n'])
    extend_([u'         <li>Post:<br>\n'])
    extend_([u'             <form action = "/admin" method="POST" enctype="multipart/form-data"> \n'])
    if post_id:
        extend_(['             ', u'<input type="hidden" name="action" value="editpost"/>\n'])
        extend_(['             ', u'<p>Id: ', escape_(post_id, True), u'</p>\n'])
    else:
        extend_(['             ', u'<input type="hidden" name="action" value="newpost"/>\n'])
    extend_([u'             <input type="hidden" name="post_id" value="', escape_(post_id, True), u'"/>\n'])
    extend_([u'             <p>title:<br><input type="text" name="title" value="', escape_(title, True), u'"/></p>\n'])
    extend_([u'             <p>link:<br> <input type="text" name="link" value="', escape_(link, True), u'"/></p>\n'])
    extend_([u'             <p>description :<br><input type="text" name="description" maxlenght="500" value="', escape_(description, True), u'"/></p>\n'])
    extend_([u'             <p>tags:<br><input type="text" name="tags" value = "', escape_(' '.join(tags), True), u'"/> </p>\n'])
    extend_([u'             <p>categories:<br>\n'])
    extend_([u'             <select name="category">\n'])
    for category_tmp in loop.setup(settings.CATEGORIES):
        extend_(['                 ', u'<option ', escape_((category_tmp==category and 'selected="selected"'), False), u'  value="', escape_(category_tmp, True), u'">', escape_(category_tmp, True), u'</option>\n'])
    extend_([u'             </select>\n'])
    extend_([u'             <p>img:<input type="file" name="img"/>\n'])
    if img_path:
        extend_(['             ', u'<img src="', escape_(img_path, True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" title="', escape_(category, True), u'" alt="Image"/><br>\n'])
        extend_(['             ', u'delete image:<input type="checkbox" name="delete_img">    \n'])
        extend_(['             ', u'\n'])
    extend_([u'             </p>\n'])
    extend_([u'             \n'])
    extend_([u'             <p>body :<br><textarea name="body" cols="40" rows="20">', escape_(body, True), u'</textarea></p>\n'])
    extend_([u'             <p><input type="submit" value="Submit"/></p>\n'])
    extend_([u'           </form>\n'])
    extend_([u'         </li>\n'])
    extend_([u'         \n'])
    if post_id:
        extend_(['         ', u'<li>Delete:\n'])
        extend_(['         ', u'   <form action = "/admin" method="POST"> \n'])
        extend_(['         ', u'       <input type="hidden" name="action" value="deletepost"/>\n'])
        extend_(['         ', u'       <input type="hidden" name="post_id" value="', escape_(post_id, True), u'"/>\n'])
        extend_(['         ', u'       <p><input type="submit" value="Delete"/></p>\n'])
        extend_(['         ', u'   </form>\n'])
    extend_([u'            </il>\n'])
    extend_([u'     </ul>\n'])
    extend_([u'                            \n'])
    extend_([u' </div>\n'])

    return self

admin = CompiledTemplate(admin, 'app/views/admin.html')
join_ = admin._join; escape_ = admin._escape

# coding: utf-8
def feed (posts, site_updated):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="utf-8"?>\n'])
    extend_([u'<feed xmlns="http://www.w3.org/2005/Atom">\n'])
    extend_([u'<title>', escape_((settings.CMS_NAME), True), u'</title>\n'])
    extend_([u'<subtitle>', escape_((settings.SLOGAN), True), u'</subtitle>\n'])
    extend_([u'<link rel="alternate" type="text/html" href="http://', escape_((curdomain), True), u'/" />\n'])
    extend_([u'<link rel="self" type="application/atom+xml" href="http://', escape_((curdomain), True), u'/index.xml" />\n'])
    extend_([u'<id>http://', escape_((curdomain), True), u'/</id>\n'])
    extend_([u'<updated>', escape_(site_updated, True), u'</updated>\n'])
    extend_([u'<rights>Copyright \xa9 2011, ', escape_(settings.CMS_NAME, True), u'</rights>\n'])
    for post in loop.setup(posts):
        extend_([u'<entry>\n'])
        extend_([u'    <title>', escape_((post.title), True), u' - ', escape_((post.category), True), u'</title>\n'])
        extend_([u'    <link rel="alternate" type="text/html" href="http://', escape_((curdomain), True), u'/post/', escape_(post.get_path(), True), u'" />\n'])
        extend_([u'    <id>tag:', escape_((curdomain), True), u',', escape_((post.created.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u':/post/', escape_((post.key().id()), True), u'</id>\n'])
        extend_([u'    <published>', escape_((post.created.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u'</published>\n'])
        extend_([u'    <updated>', escape_((post.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u'</updated>\n'])
        extend_([u'    <author>\n'])
        extend_([u'        <name>', escape_(settings.AUTHOR_NAME, True), u')</name>\n'])
        extend_([u'        <uri>http://', escape_((curdomain), True), u'</uri> \n'])
        extend_([u'    </author>\n'])
        extend_([u'    <content type="html" xml:base="http://', escape_((curdomain), True), u'/" xml:lang="en"><![CDATA[', escape_((post.description), True), u']]></content>\n'])
        extend_([u'</entry>\n'])
    extend_([u'</feed>\n'])

    return self

feed = CompiledTemplate(feed, 'app/views/feed.xml')
join_ = feed._join; escape_ = feed._escape

# coding: utf-8
def index (posts, selected_tags = [], selected_category = '', pagination = None):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    __lineoffset__ -= 3
    def render_catqs(selected_category, front_char):
        self = TemplateResult(); extend_ = self.extend
        if selected_category :
            extend_([escape_((front_char), True), u'category=', escape_(selected_category, True), u'\n'])
        extend_([u'\n'])
        return self
    extend_([u'<div id="box_tags">\n'])
    extend_([u'     <form action = "/tag/', escape_(('/'.join(selected_tags)), True), u'" method="post">  \n'])
    extend_([u'       <p>\n'])
    extend_([u'       <b>Tags:</b>\n'])
    for tag in loop.setup(selected_tags):
        extend_(['       ', u'<a class="tag dark" href="/tag/', escape_(('/'.join(selected_tags)), True), u'?removetag=', escape_((tag), True), escape_((render_catqs(selected_category,"&")), True), u'">', escape_(tag, True), u' x</a>&raquo;\n'])
    extend_([u'       <input id="search" type="text" name="addtag"/>\n'])
    extend_([u'       </p>\n'])
    extend_([u'       <p>\n'])
    extend_([u'       <input type="radio" name="category" ', escape_((selected_category == '' and 'checked="checked"' or ""), False), u' value="" onclick="this.form.submit()" />All\n'])
    for category in loop.setup(settings.CATEGORIES):
        extend_(['       ', u'<input type="radio" name="category" value="', escape_(category, True), u'" ', escape_((selected_category != "" and category == selected_category and 'checked="checked"' or ""), False), u' onclick="this.form.submit()"/>', escape_(category, True), u'\n'])
    extend_([u'       </p>\n'])
    extend_([u'       \n'])
    extend_([u'     </form>\n'])
    extend_([u'</div>\n'])
    extend_([u'<div>      \n'])
    extend_([u'      <table class="result">          \n'])
    for post in loop.setup(posts):
        extend_(['      ', u'  <tr>\n'])
        extend_(['      ', u'        <td>\n'])
        extend_(['      ', u'          <div style="float:left">\n'])
        extend_(['      ', u'              <p>', escape_(post.created.strftime("%m %B, %Y"), True), u'\n'])
        if admin:
            extend_(['                    ', u'<a href="/admin?action=editpost_init&amp;post_id=', escape_(post.key().id(), True), u'"><img src="/images/edit.png" title="Edit" alt="Edit"/></a>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'              <p><span class="main_link"><a href="', escape_(post.link, True), u'">', escape_((post.title), True), u'</a></span> | <a style="font-size:90%" href="/post/', escape_(post.get_path(), True), u'">DETAILS</a></p>\n'])
        extend_(['      ', u'              <p><a href="', escape_((post.link), True), u'">', escape_((post.link), True), u'</a></p>\n'])
        extend_(['      ', u'              <p>', escape_((post.description), True), u'</p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div style="float:right">\n'])
        extend_(['      ', u'              <p style="text-align:right;">\n'])
        extend_(['      ', u'                  <img src="', escape_(post.get_image_path(), True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" title="', escape_(post.category, True), u'" alt="Image"/>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div class="meta">\n'])
        extend_(['      ', u'              <span>\n'])
        extend_(['      ', u'                  <a class="category" href="/?category=', escape_((post.category), True), u'">', escape_((post.category), True), u'</a>\n'])
        extend_(['      ', u'              </span>\n'])
        extend_(['      ', u'              <span class="tags">\n'])
        for tag in loop.setup(post.tags):
            if tag in selected_tags:
                extend_(['                          ', u'<a class="tag dark" href="/tag/', escape_(('/'.join(selected_tags)), True), escape_((render_catqs(selected_category,"?")), True), u'">', escape_((tag), True), u'</a>\n'])
            else:
                extend_(['                          ', u'<a class="tag" href="/tag/', escape_(('/'.join(selected_tags)), True), u'?addtag=', escape_((tag), True), escape_((render_catqs(selected_category,"&")), True), u'">', escape_((tag), True), u'</a>\n'])
        extend_(['      ', u'              </span>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'        </td>\n'])
        extend_(['      ', u'   </tr>\n'])
        if loop.last:
            extend_(['         ', u'   </table>\n'])
            extend_(['         ', u'   <table class="pagination">\n'])
            extend_(['         ', u'       <tr>\n'])
            extend_(['         ', u'           <td class="pagination_page">\n'])
            if pagination.has_previous_entries():
                extend_(['                        ', u'    <a href="?page=', escape_((pagination.page-1), True), escape_((render_catqs(selected_category,"&")), True), u'">&laquo; prev&nbsp;&nbsp;</a>\n'])
            for page in loop.setup(pagination.get_pretty_pagination()):
                if page != -1:
                    extend_(['                        ', u'<a href="?page=', escape_((page), True), escape_((render_catqs(selected_category,"&")), True), u'">\n'])
                    if page == pagination.page:
                        extend_(['                            ', u'|', escape_((page), True), u'|    \n'])
                    else:
                        extend_(['                            ', escape_(page, True), u' \n'])
                    extend_(['                        ', u'</a>\n'])
                else:
                    extend_(['                        ', escape_(pagination.separator, True), u'\n'])
            if pagination.has_more_entries():
                extend_(['                        ', u'       <a href="?page=', escape_((pagination.page+1), True), escape_((render_catqs(selected_category,"&")), True), u'">&nbsp;&nbsp;next &raquo;</a>\n'])
            extend_(['         ', u'           </td>\n'])
            extend_(['         ', u'       </tr>\n'])
            extend_(['         ', u'       <tr>\n'])
            extend_(['         ', u'           <td class="pagination_found">Posts: ', escape_(commify(pagination.total), True), u'</td>\n'])
            extend_(['         ', u'       </tr>\n'])
            extend_(['         ', u'   </table>\n'])
    else:
        if len(posts) == 0:
            extend_(['        ', u'<tr>\n'])
            extend_(['        ', u'    <td>\n'])
            extend_(['        ', u'   <p id="not_found">\n'])
            extend_(['        ', u'       No posts found\n'])
            extend_(['        ', u'    </p>\n'])
            extend_(['        ', u'    </td>\n'])
            extend_(['        ', u'</tr>\n'])
            extend_(['        ', u'</table>\n'])
            extend_(['        ', u'\n'])
            extend_(['        ', u'\n'])
    extend_([u' </div>\n'])

    return self

index = CompiledTemplate(index, 'app/views/index.html')
join_ = index._join; escape_ = index._escape

# coding: utf-8
def layout (content, title = None , tag_cloud = [], categories = [], navbar = True, posts_total_count = 0, admin = None):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'])
    extend_([u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">\n'])
    extend_([u'<head>\n'])
    extend_([u'    <link rel="alternate" type="application/atom+xml" href="/index.xml" />\n'])
    extend_([u'    <meta http-equiv="content-type" content="', escape_(settings.HTML_MIME_TYPE, True), u'"/>\n'])
    extend_([u'    <meta name="description" content="', escape_((settings.META_DESCRIPTION), True), u'"/>\n'])
    extend_([u'    <meta name="keywords" content="', escape_(settings.META_KEYWORDS, True), u'"/>\n'])
    extend_([u'    <title> ', escape_((title), True), u' - ', escape_(settings.CMS_NAME, True), u'</title> \n'])
    extend_([u'    <link rel="stylesheet" href="/stylesheets/screen.css"/>\n'])
    extend_([u'    <link rel="stylesheet" href="/stylesheets/jquery.autocomplete.css"/>\n'])
    extend_([u'    <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico"/>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery-1.4.2.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery.autocomplete.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery.stacktack.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/main.js"></script>\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'<div id="header">\n'])
    extend_([u'    <h1>', escape_(settings.CMS_NAME, True), u' <img src="/images/lab.png" alt="Lab"/></h1>\n'])
    extend_([u'    <h2>', escape_((settings.SLOGAN), True), u'</h2>\n'])
    extend_([u'    <ul>\n'])
    extend_([u'        <li><a href="/" ', escape_((title=='Home' and 'class="active"' or ''), False), u'>Home</a></li>\n'])
    extend_([u'        <li><a href="/post" ', escape_(((title not in ('Home','Tag cloud','About','Admin')) and 'class="active"' or ''), False), u'>Posts</a></li>\n'])
    extend_([u'        <li><a href="/tagcloud" ', escape_((title=='Tag cloud' and 'class="active"' or ''), False), u'>Tag cloud</a></li>\n'])
    extend_([u'        <li><a href="/about" ', escape_((title=='About' and 'class="active"' or ''), False), u'>About</a></li>\n'])
    if admin:
        extend_(['        ', u'<li><a href="/admin" ', escape_((title=='Admin' and 'class="active"' or ''), False), u'>Admin</a></li>\n'])
    extend_([u'    </ul>\n'])
    extend_([u'        \n'])
    extend_([u'        <form id="form" action="http://www.google.com/cse" method="get">\n'])
    extend_([u'          <p id="layoutdims">  \n'])
    extend_([u'                <input type="hidden" name="cx" value="', escape_(settings.GOOGLE_CSE, True), u'" />\n'])
    extend_([u'            <input type="hidden" name="ie" value="UTF-8" />\n'])
    extend_([u'                <input id="search_box" name="q" tabindex="1" onfocus="if (this.value==\'search\') this.value = \'\'" type="text" maxlength="140" size="32" value="search"/>\n'])
    extend_([u'            </p>\n'])
    extend_([u'        </form>\n'])
    extend_([u'        \n'])
    extend_([u'    \n'])
    extend_([u'</div>\n'])
    if navbar:
        extend_([u'<div class="colmask rightmenu">\n'])
        extend_([u'    <div class="colleft">\n'])
        extend_([u'        <div class="col1">\n'])
        extend_([u'            ', escape_(content, False), u'\n'])
        extend_([u'        </div>    \n'])
        extend_([u'        <div class="col2">\n'])
        extend_([u'            <div id="logo">\n'])
        extend_([u'                <a href="http://code.google.com/appengine/">\n'])
        extend_([u'                    <img src="/images/google-app-engine.png" width="100" height="100" alt="Google App Engine" />\n'])
        extend_([u'                </a>\n'])
        extend_([u'            </div>\n'])
        extend_([u'            <div>\n'])
        extend_([u'                ', escape_(safemarkdown(settings.DESCRIPTION), False), u'\n'])
        extend_([u'            </div>\n'])
        extend_([u'            <p>Posts: <span class="summarycount">', escape_(commify(posts_total_count), True), u'</span></p> \n'])
        extend_([u'            <h2>Categories</h2>\n'])
        extend_([u'            <ul>\n'])
        for category in loop.setup(categories):
            extend_(['            ', u'<li><a href="/?category=', escape_(category.name, True), u'">', escape_(category.name, True), u'</a>(', escape_((category.counter), True), u')</li>\n'])
        extend_([u'            </ul>\n'])
        extend_([u'            <h2>Tags</h2>\n'])
        extend_([u'            <p>\n'])
        for tag in loop.setup(tag_cloud):
            extend_(['                ', u'    <a href="/tag/', escape_((tag.name), True), u'">', escape_((tag.name), True), u'</a>(', escape_((tag.counter), True), u')&nbsp;\n'])
            extend_(['                ', u'\n'])
        if len(tag_cloud)>=settings.NAVBAR_CLOUDSIZE:
            extend_(['                ', u'<a href="/tagcloud">more \xbb</a>\n'])
        extend_([u'            </p>\n'])
        extend_([u'            <div id="img" style="margin-top:40px">\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <a href="/feed/index.rss"><img width="45" height="45" src="/images/rss.png" alt="Rss"/></a>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <a href="http://webpy.org"><img width="80" height="30" src="/images/webpy.jpg" alt="Webpy"/></a>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <a href="http://code.google.com/appengine/"><img width="100" height="30" src="/images/appengine.png" alt="Appengine"/></a>\n'])
        extend_([u'                </p>\n'])
        extend_([u'            </div>\n'])
        extend_([u'        </div>\n'])
        extend_([u'    </div>\n'])
        extend_([u'</div>\n'])
    else:
        extend_([u'<div class="colmask fullpage">\n'])
        extend_([u'    <div class="col1">\n'])
        extend_([u'        ', escape_(content, False), u'\n'])
        extend_([u'    </div>\n'])
        extend_([u'</div>\n'])
        extend_([u'\n'])
    extend_([u'<div id="footer">\n'])
    extend_([u'    <p>\xa9 ', escape_(settings.AUTHOR_NAME, True), u' | Powered by Google App Engine\n'])
    extend_([u'    | <a href="http://jigsaw.w3.org/css-validator/check/referer">CSS</a> | <a href="http://validator.w3.org/check/referer">XHTML</a></p>\n'])
    extend_([u'</div>\n'])
    extend_([u'\n'])
    if settings.ANALYTICS_ID and not DEVEL and not admin:
        extend_([u'<script type="text/javascript">\n'])
        extend_([u'var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");\n'])
        extend_([u'document.write(unescape("%3Cscript src=\'" + gaJsHost + "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));\n'])
        extend_([u'</script>\n'])
        extend_([u'<script type="text/javascript">\n'])
        extend_([u'try {\n'])
        extend_([u'var pageTracker = _gat._getTracker("', escape_(settings.ANALYTICS_ID, True), u'");\n'])
        extend_([u'pageTracker._trackPageview();\n'])
        extend_([u'} catch(err) {}</script>\n'])
        extend_([u'\n'])
    if settings.CLICKY_ID and not DEVEL and not admin:
        extend_([u'<script src="http://static.getclicky.com/js" type="text/javascript"></script>\n'])
        extend_([u'<script type="text/javascript">clicky.init(', escape_(settings.CLICKY_ID, True), u');</script>\n'])
        extend_([u'<noscript><p><img alt="Clicky" width="1" height="1" src="http://in.getclicky.com/250663ns.gif" /></p></noscript>\n'])
        extend_([u'\n'])
        extend_([u'\n'])
        extend_([u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

layout = CompiledTemplate(layout, 'app/views/layout.html')
join_ = layout._join; escape_ = layout._escape

# coding: utf-8
def oops (message):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<div id="oops">                                                    \n'])
    extend_([u'          <p>', escape_(settings.RELAXING_MESSAGE_ERROR, True), u'</p>\n'])
    extend_([u'          <p><img src="/images/oops.png" alt="Error"/></p>\n'])
    extend_([u'          <p>', escape_((message), True), u' </p>\n'])
    extend_([u'</div>\n'])

    return self

oops = CompiledTemplate(oops, 'app/views/oops.html')
join_ = oops._join; escape_ = oops._escape

# coding: utf-8
def post (post, prev_post = None, next_post = None, content_discovered = ''):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u' <div>\n'])
    extend_([u'      <p>\n'])
    extend_([u'          <table class="pagination">\n'])
    extend_([u'              <tr>\n'])
    extend_([u'                  <td class="pagination_page" style="text-align:left">\n'])
    if prev_post:
        extend_(['                      ', u'<a href="/post/', escape_(prev_post.get_path(), True), u'">&laquo; prev</a>\n'])
    if next_post:
        extend_(['                      ', u' &nbsp;<a href="/post/', escape_(next_post.get_path(), True), u'">next &raquo;</a>\n'])
    extend_([u'                  </td>\n'])
    extend_([u'              </tr>\n'])
    extend_([u'          </table>\n'])
    extend_([u'      </p>\n'])
    extend_([u'      <div>\n'])
    extend_([u'          <div style="margin-top:20px;text-align:center;font-size:140%;font-weight:bold">\n'])
    extend_([u'          <p>', escape_((post.title), True), u'</p>\n'])
    extend_([u'              <div style="float:right;">\n'])
    extend_([u'                <img src="', escape_(post.get_image_path(), True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" alt="Image"/>\n'])
    extend_([u'              </div>\n'])
    extend_([u'          </div>\n'])
    extend_([u'          <p>', escape_(post.created.strftime("%m %B, %Y"), True), u'\n'])
    if admin:
        extend_(['              ', u'<a href="/admin?action=editpost_init&amp;post_id=', escape_(post.key().id(), True), u'"><img src="/images/edit.png" title="Edit" alt="Edit"/></a>\n'])
    extend_([u'          </p>\n'])
    extend_([u'          <p><a class="category" href="/?category=', escape_((post.category), True), u'">', escape_((post.category), True), u'</a>\n'])
    for tag in loop.setup(post.tags):
        extend_(['              ', u'  <a class="tag" href="/tag/', escape_(tag, True), u'">', escape_((tag), True), u'</a> \n'])
    extend_([u'          </p>\n'])
    extend_([u'          <p><a href="', escape_((post.link), True), u'">', escape_((post.link), True), u'</a></p>\n'])
    extend_([u'          <p>', escape_((post.description), True), u'</p>\n'])
    extend_([u'      </div>\n'])
    extend_([u'      <div>\n'])
    extend_([u'          ', escape_(safemarkdown(post.body), False), u'\n'])
    extend_([u'      </div>\n'])
    extend_([u'      <div>\n'])
    extend_([u'          ', escape_(content_discovered, False), u'\n'])
    extend_([u'      </div>\n'])
    extend_([u'      <hr>\n'])
    extend_([u' </div>\n'])
    extend_([u' <div>\n'])
    if settings.DISQUS and False:
        extend_([' ', u'<h3 id="comments">Comments</h3>\n'])
        extend_([' ', u'<div id="disqus_thread"></div>\n'])
        if development:
            extend_([' ', u'<script type="text/javascript">\n'])
            extend_([' ', u'  var disqus_developer = 1;\n'])
            extend_([' ', u'</script>\n'])
        extend_([' ', u'<script type="text/javascript" src="http://disqus.com/forums/', escape_((DISQUS), True), u'/embed.js"></script>\n'])
        extend_([' ', u'<noscript><a href="http://disqus.com/forums/', escape_((DISQUS), True), u'/?url=ref">View the discussion thread.</a></noscript>\n'])
        extend_([' ', u'<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>\n'])
    extend_([u' </div>   \n'])

    return self

post = CompiledTemplate(post, 'app/views/post.html')
join_ = post._join; escape_ = post._escape

# coding: utf-8
def tagcloud (tag_cloud):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<p>Tags found: <b>', escape_(len(tag_cloud), True), u'</b></p>\n'])
    extend_([u'<div id="main_tag_cloud">\n'])
    for tag in loop.setup(tag_cloud):
        extend_(['    ', u'    <a href="/tag/', escape_((tag.name), True), u'">', escape_((tag.name), True), u'</a>(', escape_((tag.counter), True), u')&nbsp;\n'])
        extend_(['    ', u'\n'])
    extend_([u'</div>\n'])

    return self

tagcloud = CompiledTemplate(tagcloud, 'app/views/tagcloud.html')
join_ = tagcloud._join; escape_ = tagcloud._escape

