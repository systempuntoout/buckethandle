from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def admin (submitted, result, action, title = '', link = '', description = '', tags = [], category = '', img_path ='', url_img ='', body = '', post_id ='', featured = False, markup = 'Markdown'):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' \n'])
    extend_([u' <div>\n'])
    extend_([u'     <div style="float:right">\n'])
    extend_([u'     <ul>  <li><a href="', escape_(settings.ADMIN_BOOKMARKLET, True), u'">Bookmarklet</a></li>\n'])
    extend_([u'           <li><a href="/admin/tags">Tags</a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcachestats">Memcache stats </a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcacheflush">Memcache flush </a></li>\n'])
    extend_([u'           <li><a href="/admin/content">Content discovery </a></li>\n'])
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
    extend_([u'         <p>Markup:<br>                \n'])
    extend_([u'          <select id="markup" name="markup">\n'])
    for markup_tmp in loop.setup(settings.MARKUPS):
        extend_(['          ', u'  <option ', escape_((markup==markup_tmp and 'selected="selected"'), False), u'  value="', escape_(markup_tmp, True), u'">', escape_(markup_tmp, True), u'</option>\n'])
    extend_([u'          </select>\n'])
    extend_([u'         <div>\n'])
    extend_([u'             <textarea id="post_body" name="body_Markdown" cols="80" rows="20">', escape_(body, True), u'</textarea>\n'])
    extend_([u'         </div>\n'])
    extend_([u'         <div>\n'])
    extend_([u'              <textarea id="post_body_html" name="body_Html" cols="80" rows="20">', escape_(body, True), u'</textarea>\n'])
    extend_([u'          </div>\n'])
    extend_([u'     </p>\n'])
    extend_([u'     <p><input type="submit" value="Submit"/></p>\n'])
    extend_([u'   </form>\n'])
    extend_([u'   </div>                         \n'])
    extend_([u' </div>\n'])

    return self

admin = CompiledTemplate(admin, 'app/views/admin/admin.html')
join_ = admin._join; escape_ = admin._escape

# coding: utf-8
def admin_content (submitted, result, action, feeds, posts, name = '', link = ''):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' \n'])
    extend_([u' <div>\n'])
    extend_([u'     <div style="float:right">\n'])
    extend_([u'     <ul> \n'])
    extend_([u'           <li><a href="/admin">Main admin</a></li>\n'])
    extend_([u'           <li><a href="/admin/content">Content discovery</a></li>\n'])
    extend_([u'           <li><a class="toggle" href="#">Manage Feeds</a></li>\n'])
    extend_([u'           <li><a href="/admin/content?action=start_downloadfeeds">Download Feeds entries</a></li>\n'])
    extend_([u'     </ul>\n'])
    extend_([u'     <br/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'    <div>\n'])
    if result:
        extend_(['    ', u'<div id="admin_message_box" ', escape_((submitted and 'class="admin_message_OK"' or 'class="admin_message_KO"'), False), u'>\n'])
        extend_(['    ', u' <p>RESULT: ', escape_(action, True), u'</p>\n'])
        extend_(['    ', u' <ul>\n'])
        for key in loop.setup(result.keys()):
            extend_(['     ', u'<li> ', escape_(("%s - %s" % (key, result[key])), True), u'</li>\n'])
        extend_(['    ', u' </ul>\n'])
        extend_(['    ', u'</div>\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <div class="totoggle" style="display: none">    \n'])
    extend_([u'    <form action = "/admin/content" method="POST" enctype="multipart/form-data"> \n'])
    extend_([u'        <input type="hidden" id="action" name="action" value="newfeed"/>\n'])
    extend_([u'        <p>name: <span class="required">*</span><br><input type="text" size="100" name="name" value="', escape_(name, True), u'"/></p>\n'])
    extend_([u'        <p>link: <span class="required">*</span><br> <input type="text" size="100" id = "link" name="link" value="', escape_(link, True), u'"/></p>\n'])
    extend_([u'        <p><input type="submit" value="Submit"/></p>\n'])
    extend_([u'   </form>\n'])
    extend_([u'   Feeds\n'])
    extend_([u'   <ul> \n'])
    for feed in loop.setup(feeds):
        extend_(['       ', u'<li><a href="', escape_(feed.link, True), u'">', escape_(feed.name, True), u'</a></li>\n'])
    extend_([u'   </ul>\n'])
    extend_([u'   </div>\n'])
    extend_([u'   <hr>\n'])
    extend_([u'   <table class="feed_items">\n'])
    for post in loop.setup(posts):
        extend_(['   ', u' <tr id="', escape_(post.key(), True), u'" class="', escape_(loop.parity, True), u'">\n'])
        extend_(['   ', u'   <td>', escape_((post.created.strftime("%Y-%m-%d %H:%M:%S")), True), u'</a></td>  \n'])
        extend_(['   ', u'   <td>', escape_((post.feed.name), True), u'</a></td>    \n'])
        extend_(['   ', u'   <td><a target="_blank" href="', escape_((post.link), True), u'">', escape_((post.title), True), u'</a></td>\n'])
        extend_(['   ', u'   <td><a href="#" onclick="feeditemRemove(\'', escape_(post.key(), True), u'\')" >Remove</a></td> \n'])
        extend_(['   ', u' </tr>\n'])
    else:
        if len(posts) == 0:
            extend_(['    ', u'<tr>\n'])
            extend_(['    ', u'  <td><p id="not_found">No posts found</p></td>\n'])
            extend_(['    ', u'</tr>\n'])
    extend_([u'   <table>\n'])
    extend_([u'   </div>\n'])
    extend_([u'        \n'])
    extend_([u'                            \n'])
    extend_([u' </div>\n'])

    return self

admin_content = CompiledTemplate(admin_content, 'app/views/admin/admin_content.html')
join_ = admin_content._join; escape_ = admin_content._escape

# coding: utf-8
def admin_tags (submitted, result, action):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u' \n'])
    extend_([u' <div>\n'])
    extend_([u'     <div style="float:right">\n'])
    extend_([u'     <ul>  <li><a href="', escape_(settings.ADMIN_BOOKMARKLET, True), u'">Bookmarklet</a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcachestats">Memcache stats </a></li>\n'])
    extend_([u'            <li><a href="/admin/tags">Tags</a></li>\n'])
    extend_([u'           <li><a href="/admin?action=memcacheflush">Memcache flush </a></li>\n'])
    extend_([u'           <li><a href="/admin/content">Content discovery </a></li>\n'])
    extend_([u'     </ul>    \n'])
    extend_([u'    </div>\n'])
    extend_([u'    <div>\n'])
    if result:
        extend_(['    ', u'<div id="admin_message_box" ', escape_((submitted and 'class="admin_message_OK"' or 'class="admin_message_KO"'), False), u'>\n'])
        extend_(['    ', u' <p>RESULT: ', escape_(action, True), u'</p>\n'])
        extend_(['    ', u' <ul>\n'])
        for key in loop.setup(result.keys()):
            extend_(['     ', u'<li> ', escape_(("%s - %s" % (key, result[key])), True), u'</li>\n'])
        extend_(['    ', u' </ul>\n'])
        extend_(['    ', u'</div>\n'])
    extend_([u'    <form action = "/admin/tags" method="POST"> \n'])
    extend_([u'     <input type="hidden" id="action" name="action" value="renametags_init"/>    \n'])
    extend_([u'     <p>Tags list to rename:<br><input type="text" id="tags_to_rename" name="tags_to_rename" size="100"/> </p>\n'])
    extend_([u'     <p>Tag destination:<br><input type="text" id="tag_destination" name="tag_destination" size="20" value = ""/> </p>\n'])
    extend_([u'     <p><input type="submit" value="Rename"/></p>\n'])
    extend_([u'   </form>\n'])
    extend_([u'   <hr/>\n'])
    extend_([u'   <li><a href="/admin/tags?action=deletetags">Delete ghost tags</a></li>\n'])
    extend_([u'   \n'])
    extend_([u'   \n'])
    extend_([u'   </div>\n'])
    extend_([u'        \n'])
    extend_([u'                            \n'])
    extend_([u' </div>\n'])

    return self

admin_tags = CompiledTemplate(admin_tags, 'app/views/admin/admin_tags.html')
join_ = admin_tags._join; escape_ = admin_tags._escape

# coding: utf-8
def markdown_preview (data):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'])
    extend_([u'<html xmlns="http://www.w3.org/1999/xhtml">\n'])
    extend_([u'<head>\n'])
    extend_([u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'])
    extend_([u'<title>markItUp! preview template</title>\n'])
    extend_([u'<link rel="stylesheet" type="text/css" href="~/templates/preview.css" />\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([escape_(safemarkdown(data), False), u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

markdown_preview = CompiledTemplate(markdown_preview, 'app/views/admin/markdown_preview.html')
join_ = markdown_preview._join; escape_ = markdown_preview._escape

