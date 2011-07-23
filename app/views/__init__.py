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
def admin (submitted, result, action, title = '', link = '', description = '', tags = [], category = '', img_path ='', url_img ='', body = '', post_id ='', featured = False):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' \n'])
    extend_([u' <div>\n'])
    extend_([u'     <div style="float:right">\n'])
    extend_([u'     <ul>  <li><a href="', escape_(settings.ADMIN_BOOKMARKLET, True), u'">Bookmarklet</a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcachestats">Memcache stats </a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcacheflush">Memcache flush </a></li>\n'])
    extend_([u'     </ul>\n'])
    extend_([u'     <ul>\n'])
    if post_id:
        extend_(['          ', u'<li><a href="/admin?action=deletepost&amp;post_id=', escape_((post_id), True), u'">Delete this post</a></li>\n'])
    extend_([u'      </ul>     \n'])
    extend_([u'    </div>\n'])
    extend_([u'    <div>\n'])
    if result:
        extend_(['    ', u'<div id="admin_message_box" ', escape_((submitted and 'class="admin_message_OK"' or 'class="admin_message_KO"'), False), u'>\n'])
        extend_(['    ', u' <p>RESULT: ', escape_(action, True), u'</p>\n'])
        extend_(['    ', u' <ul>\n'])
        for key in loop.setup(result.keys()):
            extend_(['     ', u'<li> ', escape_(("%s - %s" % (key, result[key])), True), u'</li>\n'])
        extend_(['    ', u' </ul>\n'])
        extend_(['    ', u'</div>    \n'])
    extend_([u'    <form action = "/admin" method="POST" enctype="multipart/form-data"> \n'])
    extend_([u'     <input type="hidden" name="post_id" value="', escape_(post_id, True), u'"/>\n'])
    if post_id:
        extend_(['     ', u'<input type="hidden" id="action" name="action" value="editpost"/>\n'])
    else:
        extend_(['     ', u'<input type="hidden" id="action" name="action" value="newpost"/>\n'])
    extend_([u'     <p>title: <span class="required">*</span><br><input type="text" size="100" name="title" value="', escape_(title, True), u'"/></p>\n'])
    extend_([u'     <p>link: <br> <input type="text" size="100" id = "link" name="link" value="', escape_(link, True), u'"/> <span id="link_check"/></p>\n'])
    extend_([u'     <p>description :<br><input type="text" size="150" name="description" maxlenght="500" value="', escape_(description, True), u'"/></p>\n'])
    extend_([u'     <p>tags:<br><input type="text" id="tags" name="tags" size="100" value = "', escape_(' '.join(tags), True), u'"/> </p>\n'])
    extend_([u'     <p>featured:<br><input type="checkbox" id="featured" name="featured" ', escape_((featured and 'checked="checked"'), False), u'/> </p>\n'])
    if settings.CATEGORIES:
        extend_(['     ', u'<p>categories:<br>\n'])
        extend_(['     ', u'<select name="category">\n'])
        for category_tmp in loop.setup(settings.CATEGORIES):
            extend_(['         ', u'<option ', escape_((category_tmp==category and 'selected="selected"'), False), u'  value="', escape_(category_tmp, True), u'">', escape_(category_tmp, True), u'</option>\n'])
        extend_(['     ', u'</select>\n'])
    extend_([u'     <p>img:<br><input type="file" size="100" name="img"/></p>\n'])
    extend_([u'     <p>\n'])
    if img_path:
        extend_(['     ', u'<img src="', escape_(img_path, True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" title="', escape_(category, True), u'" alt="Image"/><br>\n'])
        extend_(['     ', u'delete image:<br><input type="checkbox" name="delete_img">    \n'])
    extend_([u'     </p>\n'])
    extend_([u'     <p>\n'])
    extend_([u'         url_img:<br><input type="text" size="100" name="url_img" value="', escape_(url_img, True), u'"/>\n'])
    extend_([u'     </p>\n'])
    extend_([u'     \n'])
    extend_([u'     <p>body :<br>\n'])
    extend_([u'         <div>\n'])
    extend_([u'             <textarea id="post_body" name="body" cols="80" rows="20">', escape_(body, True), u'</textarea>\n'])
    extend_([u'         </div>\n'])
    extend_([u'     </p>\n'])
    extend_([u'     <p><input type="submit" value="Submit"/></p>\n'])
    extend_([u'   </form>\n'])
    extend_([u'   </div>\n'])
    extend_([u'        \n'])
    extend_([u'                            \n'])
    extend_([u' </div>\n'])

    return self

admin = CompiledTemplate(admin, 'app/views/admin.html')
join_ = admin._join; escape_ = admin._escape

# coding: utf-8
def cse():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="UTF-8" ?>\n'])
    extend_([u'<GoogleCustomizations>\n'])
    extend_([u'  <CustomSearchEngine volunteers="false" visible="false" encoding="utf-8">\n'])
    extend_([u'    <Title>', escape_((settings.CMS_NAME), True), u'</Title>\n'])
    extend_([u'    <Description>', escape_((settings.SLOGAN), True), u'</Description>\n'])
    extend_([u'    <Context>\n'])
    extend_([u'      <BackgroundLabels>\n'])
    extend_([u'        <Label name="cse_include" mode="FILTER" />\n'])
    extend_([u'        <Label name="cse_exclude" mode="ELIMINATE" />\n'])
    extend_([u'      </BackgroundLabels>\n'])
    extend_([u'    </Context>\n'])
    extend_([u'    <LookAndFeel nonprofit="false" />\n'])
    if settings.ADSENSE_ID:
        extend_(['    ', u'<AdSense>\n'])
        extend_(['    ', u' <Client id="', escape_((settings.ADSENSE_ID), True), u'">\n'])
        if settings.ADSENSE_CHANNEL_ID:
            extend_(['       ', u'<Channel id="', escape_((settings.ADSENSE_CHANNEL_ID), True), u'"/>\n'])
        extend_(['    ', u'</Client>\n'])
        extend_(['    ', u'</AdSense>\n'])
    extend_([u'  </CustomSearchEngine>  \n'])
    extend_([u'  <Annotations>\n'])
    extend_([u'    <Annotation about="http://', escape_((settings.HOST), True), u'/*">\n'])
    extend_([u'      <Label name="cse_include" />\n'])
    extend_([u'    </Annotation>\n'])
    extend_([u'  </Annotations>\n'])
    extend_([u'</GoogleCustomizations>\n'])

    return self

cse = CompiledTemplate(cse, 'app/views/cse.xml')
join_ = cse._join; escape_ = cse._escape

# coding: utf-8
def featured (posts, is_user_admin = False):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<div>      \n'])
    extend_([u'      <table class="result" style="margin-top:40px">          \n'])
    for post in loop.setup(posts):
        extend_(['      ', u'  <tr>\n'])
        extend_(['      ', u'        <td>\n'])
        extend_(['      ', u'          <div style="overflow: hidden;">\n'])
        extend_(['      ', u'          <div style="float:left;width:90%">\n'])
        extend_(['      ', u'              <p>', escape_(post.created.strftime("%d %B, %Y"), True), u'\n'])
        if is_user_admin:
            extend_(['                    ', u'<a href="/admin?action=editpost_init&amp;post_id=', escape_(post.key(), True), u'"><img src="/images/edit.png" title="Edit" alt="Edit"/></a>\n'])
            extend_(['                    ', u'| <a style="font-size:90%" href="/post/', escape_(post.get_path(), True), u'">DETAILS</a>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'              <p>\n'])
        if post.link:
            extend_(['                    ', u'<span class="main_link"><a href="', escape_(post.link, True), u'">', escape_((post.title), True), u'</a></span>\n'])
        else:
            extend_(['                    ', u'<span class="main_title">', escape_((post.title), True), u'</span>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'              <p><a target="_blank" href="', escape_((post.link), True), u'">', escape_((post.link), True), u'</a></p>\n'])
        extend_(['      ', u'              <p>', escape_((post.description), True), u'</p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div style="float:right">\n'])
        extend_(['      ', u'              <p style="text-align:right;">\n'])
        extend_(['      ', u'                  <img src="', escape_(post.get_image_path(), True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" title="', escape_(post.category, True), u'" alt="Image"/>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div class="meta">\n'])
        if settings.CATEGORIES:
            extend_(['                    ', u'<span>\n'])
            extend_(['                    ', u'    <a class="category" href="/?category=', escape_((post.category), True), u'">', escape_((post.category), True), u'&nbsp;<img width="17px" height="17px" src="', escape_((utils.get_predefined_image_link(category = post.category)), True), u'"/></a>\n'])
            extend_(['                    ', u'</span>\n'])
        extend_(['      ', u'              <span class="tags">\n'])
        for tag in loop.setup(post.tags):
            extend_(['                        ', u'<a class="tag" href="/tag/', escape_(tag, True), u'">', escape_((tag), True), u'</a> \n'])
        extend_(['      ', u'              </span>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'        </td>\n'])
        extend_(['      ', u'   </tr>\n'])
        if loop.last:
            extend_(['         ', u'   </table>\n'])
            extend_(['         ', u'   <table class="pagination">\n'])
            extend_(['         ', u'       <tr>\n'])
            extend_(['         ', u'           <td class="pagination_found">Posts: ', escape_(commify(len(posts)), True), u'</td>\n'])
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

featured = CompiledTemplate(featured, 'app/views/featured.html')
join_ = featured._join; escape_ = featured._escape

# coding: utf-8
def feed (posts, site_updated):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="utf-8"?>\n'])
    extend_([u'<feed xmlns="http://www.w3.org/2005/Atom">\n'])
    extend_([u'<title>', escape_((settings.CMS_NAME), True), u'</title>\n'])
    extend_([u'<subtitle>', escape_((settings.SLOGAN), True), u'</subtitle>\n'])
    extend_([u'<link rel="alternate" type="text/html" href="http://', escape_((settings.HOST), True), u'/" />\n'])
    extend_([u'<link rel="self" type="application/atom+xml" href="http://', escape_((settings.HOST), True), u'/index.xml" />\n'])
    extend_([u'<id>http://', escape_((settings.HOST), True), u'/</id>\n'])
    extend_([u'<updated>', escape_(site_updated, True), u'</updated>\n'])
    extend_([u'<rights>Copyright \xa9 2011, ', escape_(settings.CMS_NAME, True), u'</rights>\n'])
    for post in loop.setup(posts):
        extend_([u'<entry>\n'])
        extend_([u'    <title>', escape_((post.title), True), u' - ', escape_((post.category), True), u'</title>\n'])
        extend_([u'    <link rel="alternate" type="text/html" href="http://', escape_((settings.HOST), True), u'/post/', escape_(post.get_path(), True), u'" />\n'])
        extend_([u'    <id>tag:', escape_((settings.HOST), True), u',', escape_((post.created.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u':/post/', escape_((post.key()), True), u'</id>\n'])
        extend_([u'    <published>', escape_((post.created.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u'</published>\n'])
        extend_([u'    <updated>', escape_((post.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")), True), u'</updated>\n'])
        extend_([u'    <author>\n'])
        extend_([u'        <name>', escape_(settings.AUTHOR_NAME, True), u'</name>\n'])
        extend_([u'        <uri>http://', escape_((settings.HOST), True), u'</uri> \n'])
        extend_([u'    </author>\n'])
        extend_([u'    <content type="html" xml:base="http://', escape_((settings.HOST), True), u'/" xml:lang="en"><![CDATA[', escape_((post.description), True), u']]></content>\n'])
        extend_([u'</entry>\n'])
    extend_([u'</feed>\n'])

    return self

feed = CompiledTemplate(feed, 'app/views/feed.xml')
join_ = feed._join; escape_ = feed._escape

# coding: utf-8
def index (posts, selected_tags = [], selected_category = '', pagination = None, is_user_admin = False):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    __lineoffset__ -= 3
    def render_catqs(selected_category, front_char):
        self = TemplateResult(); extend_ = self.extend
        if selected_category :
            extend_([escape_((front_char), False), u'category=', escape_(selected_category, True), u'\n'])
        extend_([u'\n'])
        return self
    extend_([u'<div id="box_tags">\n'])
    extend_([u'     <form action = "/tag/', escape_(urlquote('/'.join(selected_tags)), True), u'" method="post">  \n'])
    extend_([u'       <p>\n'])
    extend_([u'       <b>Tags:</b>\n'])
    for tag in loop.setup(selected_tags):
        extend_(['       ', u'<a class="tag dark" href="/tag/', escape_(urlquote('/'.join(selected_tags)), True), u'?removetag=', escape_(urlquote(tag), True), escape_((render_catqs(selected_category,"&")), True), u'">', escape_(tag, True), u' x</a>&raquo;\n'])
    extend_([u'       <input id="search" type="text" size="35" name="addtag"/>\n'])
    extend_([u'       </p>\n'])
    if settings.CATEGORIES:
        extend_(['       ', u'<div>\n'])
        extend_(['       ', u' <ul id="category_list">\n'])
        extend_(['       ', u' <li>\n'])
        extend_(['       ', u'   <label ', escape_((selected_category == '' and 'id="selected_category"' or ""), False), u' for="All">\n'])
        extend_(['       ', u'   <input type="radio" id="All" name="category" ', escape_((selected_category == '' and 'checked="checked"' or ""), False), u' value="" onclick="this.form.submit()" />\n'])
        extend_(['       ', u'   All</label>\n'])
        extend_(['       ', u' </li>\n'])
        for category in loop.setup(settings.CATEGORIES):
            extend_(['          ', u'<li>\n'])
            extend_(['          ', u'<label ', escape_((selected_category != "" and category == selected_category and 'id="selected_category"' or ""), False), u' for="', escape_(category, True), u'">\n'])
            extend_(['          ', u'<input type="radio" name="category" id="', escape_(category, True), u'" value="', escape_(category, True), u'" ', escape_((selected_category != "" and category == selected_category and 'checked="checked"' or ""), False), u' onclick="this.form.action= this.form.action+\'?category=\' + this.value; this.form.submit();"/>\n'])
            extend_(['          ', escape_(category, True), u'</label>\n'])
            extend_(['          ', u'</li>              \n'])
        extend_(['       ', u' </ul>\n'])
        extend_(['       ', u' </div>\n'])
    extend_([u'     </form>\n'])
    extend_([u'</div>\n'])
    extend_([u'<div>      \n'])
    extend_([u'      <table class="result">          \n'])
    for post in loop.setup(posts):
        extend_(['      ', u'  <tr>\n'])
        extend_(['      ', u'        <td>\n'])
        extend_(['      ', u'          <div style="overflow: hidden;">\n'])
        extend_(['      ', u'          <div style="float:left;width:90%">\n'])
        extend_(['      ', u'              <p>', escape_(post.created.strftime("%d %B, %Y"), True), u'\n'])
        if is_user_admin:
            extend_(['                    ', u'<a href="/admin?action=editpost_init&amp;post_id=', escape_(post.key(), True), u'"><img src="/images/edit.png" title="Edit" alt="Edit"/></a>\n'])
        extend_(['      ', u'              | <a style="font-size:90%" href="/post/', escape_(post.get_path(), True), u'">DETAILS</a>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'              <p>\n'])
        if post.link:
            extend_(['                    ', u'<span class="main_link"><a href="', escape_(post.link, True), u'">', escape_((post.title), True), u'</a></span>\n'])
        else:
            extend_(['                    ', u'<span class="main_title">', escape_((post.title), True), u'</span>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'              <p><a target="_blank" rel="nofollow" href="', escape_((post.link), True), u'">', escape_((post.link), True), u'</a></p>\n'])
        extend_(['      ', u'              <p>', escape_((post.description), True), u'</p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div style="float:right">\n'])
        extend_(['      ', u'              <p style="text-align:right;">\n'])
        extend_(['      ', u'                  <img src="', escape_(post.get_image_path(), True), u'" width="', escape_(settings.THUMBNAIL_WIDTH, True), u'" height="', escape_(settings.THUMBNAIL_HEIGHT, True), u'" title="', escape_(post.category, True), u'" alt="Image"/>\n'])
        extend_(['      ', u'              </p>\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'\n'])
        extend_(['      ', u'          </div>\n'])
        extend_(['      ', u'          <div class="meta">\n'])
        if settings.CATEGORIES:
            extend_(['                    ', u'<span>\n'])
            extend_(['                    ', u'    <a class="category" href="/?category=', escape_((post.category), True), u'">', escape_((post.category), True), u'&nbsp;<img alt="', escape_((post.category), True), u'" width="17px" height="17px" src="', escape_((utils.get_predefined_image_link(category = post.category)), True), u'"/></a>\n'])
            extend_(['                    ', u'</span>\n'])
        extend_(['      ', u'              <span class="tags">\n'])
        for tag in loop.setup(post.tags):
            if tag in selected_tags:
                extend_(['                          ', u'<a class="tag dark" href="/tag/', escape_(urlquote('/'.join(selected_tags)), True), escape_((render_catqs(selected_category,"?")), True), u'">', escape_((tag), True), u'</a>\n'])
            else:
                extend_(['                          ', u'<a class="tag" href="/tag/', escape_(urlquote('/'.join(selected_tags)), True), u'?addtag=', escape_(urlquote(tag), True), escape_((render_catqs(selected_category,"&")), True), u'">', escape_((tag), True), u'</a>\n'])
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
            extend_(['         ', u'               [ ', escape_(pagination.page, True), u' ]\n'])
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
def layout (content, title = None , tag_cloud = [], categories = [], navbar = True, posts_total_count = 0, user = None, is_user_admin = False, login_url = '', logout_url = '', canonical = ''):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    max_occurrencies =  tag_cloud[0].counter if len(tag_cloud)>0 else 1
    extend_([u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'])
    extend_([u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">\n'])
    extend_([u'<head>\n'])
    extend_([u'    <link rel="alternate" type="application/atom+xml" href="/index.xml" />\n'])
    extend_([u'    <meta http-equiv="content-type" content="', escape_(settings.HTML_MIME_TYPE, True), u'"/>\n'])
    extend_([u'    <meta name="description" content="', escape_((settings.META_DESCRIPTION), True), u'"/>\n'])
    extend_([u'    <meta name="keywords" content="', escape_(settings.META_KEYWORDS, True), u'"/>\n'])
    extend_([u'    <title> ', escape_((title), True), u' - ', escape_(settings.CMS_NAME, True), u'</title> \n'])
    extend_([u'    <link rel="stylesheet" type="text/css" href="/stylesheets/screen.css"/>\n'])
    extend_([u'    <link rel="stylesheet" type="text/css" href="/stylesheets/jquery.autocomplete.css"/>\n'])
    extend_([u'    <link rel="stylesheet" type="text/css" href="/stylesheets/uniform.default.css"/>\n'])
    extend_([u'    <link rel="stylesheet" type="text/css" href="/javascripts/markitup/skins/markitup/style.css" />\n'])
    extend_([u'    <link rel="stylesheet" type="text/css" href="/javascripts/markitup/sets/markdown/style.css" />\n'])
    extend_([u'    <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico"/>\n'])
    if canonical:
        extend_(['    ', u'<link rel="canonical" href="http://', escape_((settings.HOST), True), u'/', escape_((canonical), True), u'"/>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery-1.4.2.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery.autocomplete.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="http://app.stacktack.com/jquery.stacktack.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="http://scripts.embed.ly/jquery.embedly.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/jquery.uniform.min.js" ></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/typewatch.js" ></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/main.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/markitup/jquery.markitup.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/javascripts/markitup/sets/markdown/set.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>\n'])
    extend_([u'    <!-- markItUp! skin -->\n'])
    extend_([u'    \n'])
    extend_([u'    \n'])
    extend_([u'    \n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'<div id="header">\n'])
    extend_([u'    <span id="login">\n'])
    if user:
        extend_(['        ', escape_(user, True), u' | <span class="login"><a href="', escape_(logout_url, True), u'">logout</a></span>\n'])
    else:
        extend_(['        ', u'<span class="login"><a href="', escape_(login_url, True), u'">login</a></span>\n'])
    extend_([u'    </span>\n'])
    extend_([u'    <h1>', escape_(settings.CMS_NAME, True), u' <img src="/images/lab.png" alt="Lab"/></h1>\n'])
    extend_([u'    <h2>', escape_((settings.SLOGAN), True), u'</h2>\n'])
    extend_([u'    <ul>\n'])
    extend_([u'        <li><a href="/" ', escape_((title=='Home' and 'class="active"' or ''), False), u'>Home</a></li>\n'])
    extend_([u'        <li><a href="/featured" ', escape_((title=='Featured' and 'class="active"' or ''), False), u'>Featured</a></li>\n'])
    extend_([u'        <li><a href="/post" ', escape_(((title not in ('Home','Tag cloud','Featured','About','Admin')) and 'class="active"' or ''), False), u'>Posts</a></li>\n'])
    extend_([u'        <li><a href="/tagcloud" ', escape_((title=='Tag cloud' and 'class="active"' or ''), False), u'>Tag cloud</a></li>\n'])
    extend_([u'        <li><a href="/about" ', escape_((title=='About' and 'class="active"' or ''), False), u'>About</a></li>\n'])
    if is_user_admin:
        extend_(['        ', u'<li><a href="/admin" ', escape_((title=='Admin' and 'class="active"' or ''), False), u'>Admin</a></li>\n'])
    extend_([u'    </ul>\n'])
    extend_([u'        \n'])
    extend_([u'        <form id="form" action="/search" method="get">\n'])
    extend_([u'          <p id="layoutdims">  \n'])
    extend_([u'            <input type="hidden" name="ie" value="UTF-8" />\n'])
    extend_([u'            <input type="hidden" name="cref" value="', escape_((settings.HOST), True), u'/cse.xml" />\n'])
    extend_([u'            <input type="hidden" name="cof" value="FORID:11" />\n'])
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
        if settings.CATEGORIES:
            extend_(['            ', u'<h2>Categories</h2>\n'])
            extend_(['            ', u'<ul>\n'])
            for category in loop.setup(categories):
                extend_(['            ', u'<li><a href="/?category=', escape_(category.name, True), u'">', escape_(category.name, True), u'</a><span class="counter">(', escape_(commify(category.counter), True), u')</span></li>\n'])
            extend_(['            ', u'</ul>\n'])
        extend_([u'            <h2>Tags</h2>\n'])
        extend_([u'            <p>\n'])
        for tag in loop.setup(tag_cloud):
            extend_(['                ', u'    <span class="tag_info"><a class="tag_cloud_nav_', escape_(utils.get_tag_weight(tag.counter,max_occurrencies), True), u'" href="/tag/', escape_((tag.name), True), u'">', escape_((tag.name), True), u'</a><span class="counter">(', escape_(commify(tag.counter), True), u')</span>&nbsp;</span>\n'])
            extend_(['                ', u'\n'])
        if len(tag_cloud)>=settings.NAVBAR_CLOUDSIZE:
            extend_(['                ', u'<br/><span class="more_tag"><a  href="/tagcloud">more \xbb</a></span>\n'])
        extend_([u'            </p>\n'])
        extend_([u'            <div id="img" style="margin-top:10px">\n'])
        extend_([u'                <p style="text-align:center">\n'])
        extend_([u'                <a href="/submit?action=submit_init"><img onmouseout="this.src=\'/images/submitlink.png\';" onmouseover="this.src=\'/images/submitlink_hover.png\'" src="/images/submitlink.png" alt="Submit a link"/></a>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <a href="/feed/index.rss"><img width="45" height="45" src="/images/rss.png" alt="Rss"/></a>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <g:plusone size="medium"></g:plusone>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                    <div class="addthis_toolbox addthis_default_style ">\n'])
        extend_([u'                    <a class="addthis_button_preferred_1"></a>\n'])
        extend_([u'                    <a class="addthis_button_preferred_2"></a>\n'])
        extend_([u'                    <a class="addthis_button_preferred_3"></a>\n'])
        extend_([u'                    <a class="addthis_button_preferred_4"></a>\n'])
        extend_([u'                    <a class="addthis_button_compact"></a>\n'])
        extend_([u'                    <a class="addthis_counter addthis_bubble_style"></a>\n'])
        extend_([u'                    </div>\n'])
        extend_([u'                    <script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#pubid=xa-4e2ac7014073bf9a"></script>\n'])
        extend_([u'                </p>\n'])
        extend_([u'                <p>\n'])
        extend_([u'                <a href="/"><img src="/images/buckethandle.png" alt="buckethandle"/></a>\n'])
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
    extend_([u'    <p>\xa9 ', escape_(settings.AUTHOR_NAME, True), u' | Powered by Google App Engine | BucketHandle v. ', escape_(settings.VERSION, True), u'</p>\n'])
    extend_([u'</div>\n'])
    extend_([u'\n'])
    if settings.ANALYTICS_ID and not development and not is_user_admin:
        extend_([u'<script type="text/javascript">\n'])
        extend_([u'  var _gaq = _gaq || [];\n'])
        extend_([u"  _gaq.push(['_setAccount', '", escape_(settings.ANALYTICS_ID, True), u"']);\n"])
        extend_([u"  _gaq.push(['_trackPageview']);\n"])
        extend_([u'  (function() {\n'])
        extend_([u"    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;\n"])
        extend_([u"    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n"])
        extend_([u"    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);\n"])
        extend_([u'  })();\n'])
        extend_([u'</script>\n'])
        extend_([u'\n'])
    if settings.CLICKY_ID and not development and not is_user_admin:
        extend_([u'<script src="http://static.getclicky.com/js" type="text/javascript"></script>\n'])
        extend_([u'<script type="text/javascript">clicky.init(', escape_(settings.CLICKY_ID, True), u');</script>\n'])
        extend_([u'<noscript><p><img alt="Clicky" width="1" height="1" src="http://in.getclicky.com/', escape_((settings.CLICKY_ID), True), u'ns.gif" /></p></noscript>\n'])
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
def post (post, prev_post = None, next_post = None, content_discovered = '', is_user_admin = False):
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
    extend_([u'          <p>', escape_(post.created.strftime("%d %B, %Y"), True), u'\n'])
    extend_([u'              <a href="/post/', escape_(post.get_path(), True), u'"><img src="/images/permalink.png" title="Permalink" alt="Permalink"/></a>\n'])
    if is_user_admin:
        extend_(['              ', u'<a href="/admin?action=editpost_init&amp;post_id=', escape_(post.key(), True), u'"><img src="/images/edit.png" title="Edit" alt="Edit"/></a>\n'])
        extend_(['              ', u'\n'])
    extend_([u'          </p>\n'])
    extend_([u'          <p>\n'])
    if settings.CATEGORIES:
        extend_(['              ', u'  <a class="category" href="/?category=', escape_((post.category), True), u'">', escape_((post.category), True), u'&nbsp;<img width="17px" height="17px" src="', escape_((utils.get_predefined_image_link(category = post.category)), True), u'"/></a>\n'])
    for tag in loop.setup(post.tags):
        extend_(['              ', u'  <a class="tag" href="/tag/', escape_(tag, True), u'">', escape_((tag), True), u'</a> \n'])
    extend_([u'          </p>\n'])
    extend_([u'          <p><a target="_blank" rel="nofollow" href="', escape_((post.link), True), u'">', escape_((post.link), True), u'</a></p>\n'])
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
    if settings.DISQUS and not development:
        extend_([' ', u'<h3 id="comments">Comments</h3>\n'])
        extend_([' ', u'<div id="disqus_thread"></div>\n'])
        if development:
            extend_([' ', u'<script type="text/javascript">\n'])
            extend_([' ', u'  var disqus_developer = 1;\n'])
            extend_([' ', u'</script>\n'])
        extend_([' ', u'<script type="text/javascript" src="http://disqus.com/forums/', escape_((settings.DISQUS), True), u'/embed.js"></script>\n'])
        extend_([' ', u'<noscript><a href="http://disqus.com/forums/', escape_((settings.DISQUS), True), u'/?url=ref">View the discussion thread.</a></noscript>\n'])
        extend_([' ', u'<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>\n'])
    extend_([u' </div>   \n'])

    return self

post = CompiledTemplate(post, 'app/views/post.html')
join_ = post._join; escape_ = post._escape

# coding: utf-8
def robots():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'User-Agent: *\n'])
    extend_([u'Disallow: /admin\n'])
    extend_([u'Sitemap: http://', escape_((settings.HOST), True), u'/sitemap_index.xml\n'])
    extend_([u'Sitemap: http://', escape_((settings.HOST), True), u'/sitemap.xml\n'])

    return self

robots = CompiledTemplate(robots, 'app/views/robots.txt')
join_ = robots._join; escape_ = robots._escape

# coding: utf-8
def search():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<div id="cse-search-results"></div>\n'])
    extend_([u'  <script type="text/javascript">\n'])
    extend_([u'    var googleSearchIframeName = "cse-search-results";\n'])
    extend_([u'    var googleSearchFormName = "cse-search-box";\n'])
    extend_([u'    var googleSearchFrameWidth = 649;\n'])
    extend_([u'    var googleSearchDomain = "www.google.com";\n'])
    extend_([u'    var googleSearchPath = "/cse";\n'])
    extend_([u'  </script>\n'])
    extend_([u'  <script type="text/javascript" src="http://www.google.com/afsonline/show_afs_search.js"></script>\n'])

    return self

search = CompiledTemplate(search, 'app/views/search.html')
join_ = search._join; escape_ = search._escape

# coding: utf-8
def sitemap (sitemap_urls):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="UTF-8"?>\n'])
    extend_([u'<urlset\n'])
    extend_([u'      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'])
    extend_([u'      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'])
    extend_([u'      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9\n'])
    extend_([u'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'])
    for url in loop.setup(sitemap_urls):
        extend_(['  ', u'<url>\n'])
        extend_(['  ', u'  <loc>http://', escape_((settings.HOST), True), escape_((url), True), u'</loc>\n'])
        extend_(['  ', u'</url>\n'])
    extend_([u'</urlset>\n'])

    return self

sitemap = CompiledTemplate(sitemap, 'app/views/sitemap.xml')
join_ = sitemap._join; escape_ = sitemap._escape

# coding: utf-8
def sitemap_index (sitemaps):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="UTF-8"?>\n'])
    extend_([u'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'])
    for sitemap in loop.setup(sitemaps):
        extend_(['  ', u'<sitemap>\n'])
        extend_(['  ', u'    <loc>http://', escape_((settings.HOST), True), u'/sitemap_', escape_((sitemap.key().id()), True), u'.xml</loc>\n'])
        extend_(['  ', u'    <lastmod>', escape_((sitemap.last_modified.strftime("%Y-%m-%d")), True), u'</lastmod>\n'])
        extend_(['  ', u'</sitemap>\n'])
    extend_([u'</sitemapindex>\n'])

    return self

sitemap_index = CompiledTemplate(sitemap_index, 'app/views/sitemap_index.xml')
join_ = sitemap_index._join; escape_ = sitemap_index._escape

# coding: utf-8
def sitemap_posts (posts):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<?xml version="1.0" encoding="UTF-8"?>\n'])
    extend_([u'<urlset\n'])
    extend_([u'      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'])
    extend_([u'      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'])
    extend_([u'      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9\n'])
    extend_([u'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'])
    for post in loop.setup(posts):
        extend_(['  ', u'<url>\n'])
        extend_(['  ', u'  <loc>http://', escape_((settings.HOST), True), u'/post/', escape_((post.get_path()), True), u'</loc>\n'])
        extend_(['  ', u'</url>\n'])
    extend_([u'</urlset>\n'])

    return self

sitemap_posts = CompiledTemplate(sitemap_posts, 'app/views/sitemap_posts.xml')
join_ = sitemap_posts._join; escape_ = sitemap_posts._escape

# coding: utf-8
def submit (submitted, message, title = '', link = '', description = '', tags = [], category = ''):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' <div>\n'])
    extend_([u'     <ul>\n'])
    extend_([u'         <li>Save this <a href="', escape_(settings.USER_BOOKMARKLET, True), u'">Bookmarklet</a> and use it to Submit a new link<br>\n'])
    extend_([u'     </ul>\n'])
    extend_([u'     <ul>     \n'])
    extend_([u'         <li>Submit a link:<br>\n'])
    extend_([u'             <form action = "/submit" method="POST"> \n'])
    extend_([u'             <input type="hidden" name="action" value="submit"/>\n'])
    extend_([u'             <p>title : <span class="required">*</span> <span class="help">[ex: tipfy ]<span><br><input type="text" size="100" name="title" value="', escape_(title, True), u'"/></p>\n'])
    extend_([u'             <p>link : <span class="required">*</span> <span class="help">[ex: http://www.tipfy.org ]<span><br> <input type="text" size="100" id = "link" name="link" value="', escape_(link, True), u'"/> <span id="link_check"/></p>\n'])
    extend_([u'             <p>description : <span class="help">[ex: tipfy is a top notch gae web-framework ]<span><br><input type="text" size="100" name="description" maxlenght="500" value="', escape_(description, True), u'"/></p>\n'])
    extend_([u'             <p>tags : <span class="required">*</span> <span class="help">[ex: python web-frameworks ]<span><br><input type="text" id="tags" name="tags" size="100" value = "', escape_(' '.join(tags), True), u'"/> </p>\n'])
    if settings.CATEGORIES:
        extend_(['             ', u'<p>categories:<br>\n'])
        extend_(['             ', u'<select name="category">\n'])
        for category_tmp in loop.setup(settings.CATEGORIES):
            extend_(['                 ', u'<option ', escape_((category_tmp==category and 'selected="selected"'), False), u'  value="', escape_(category_tmp, True), u'">', escape_(category_tmp, True), u'</option>\n'])
        extend_(['             ', u'</select>\n'])
    extend_([u'             <br/><br/>\n'])
    extend_([u'             <p><input type="submit" value="Submit a link"/></p>\n'])
    extend_([u'           </form>\n'])
    extend_([u'         </li>\n'])
    extend_([u'     </ul>\n'])
    if message:
        extend_(['     ', u'<div id="message_box">\n'])
        if submitted:
            extend_(['             ', u'<span class="message_OK">', escape_(message, True), u'</span>\n'])
        else:
            extend_(['             ', u'<span class="message_KO">', escape_(message, True), u'</span>\n'])
        extend_(['     ', u' </div>\n'])
    extend_([u' </div>\n'])

    return self

submit = CompiledTemplate(submit, 'app/views/submit.html')
join_ = submit._join; escape_ = submit._escape

# coding: utf-8
def tagcloud (tag_cloud):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    max_occurrencies =  tag_cloud[0].counter if len(tag_cloud)>0 else 1
    extend_([u'\n'])
    extend_([u'<p>Tags found: <b>', escape_(commify(len(tag_cloud)), True), u'</b></p>\n'])
    extend_([u'<p>Filter: <input type="text" id="tagcloud_filter" maxlength="20" size="20"/></p>\n'])
    extend_([u'<div id="main_tag_cloud">\n'])
    for tag in loop.setup(tag_cloud):
        extend_(['    ', u'    <span class="tag_info"><a class="tag_cloud_', escape_(utils.get_tag_weight(tag.counter,max_occurrencies), True), u'" href="/tag/', escape_((tag.name), True), u'">', escape_((tag.name), True), u'</a><span class="counter">(', escape_(commify(tag.counter), True), u')</span>&nbsp;</span>\n'])
        extend_(['    ', u'\n'])
    extend_([u'</div>\n'])

    return self

tagcloud = CompiledTemplate(tagcloud, 'app/views/tagcloud.html')
join_ = tagcloud._join; escape_ = tagcloud._escape

