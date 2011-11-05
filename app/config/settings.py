# -*- coding: utf-8 -*-
#Meta
VERSION = '0.9.0.6'
CMS_NAME = u"GAE Cupboard"
AUTHOR_NAME = u"systempuntoout"
SLOGAN = u"Ingredients for your Google App Engine recipes"
DESCRIPTION = u"""**GAE Cupboard**  
                *App Engine knowledge base directory*"""             
META_DESCRIPTION = u"GAE Cupboard - Ingredients for your Google App Engine recipes"
META_KEYWORDS = u"Gae appengine Google App Engine  libraries tutorial videos projects stackoverflow "
CATEGORIES = [u"Libraries",u"Articles",u"Books", u"Questions", u"Videos", u"Applications"]
MAIL_ADMIN = u"systempuntoout@gmail.com"
HOST = "www.gaecupboard.com" #Insert your host here: foo.appspot.com or in case of custom domain www.foo.com
REDIRECT_FROM_APPENGINE_HOST_TO_HOST = True 
APPENGINE_HOST = "gaecupboard.appspot.com" #Mandatory if REDIRECT_FROM_APPENGINE_HOST_TO_HOST is set to True

ABOUT =u"""
GAE Cupboard is a five days hack project made after a meniscus surgery ([buckethandle](http://www.leadingmd.com/patientEd/assets/buckethandle_tear.gif "buckethandle")).  
Having some time to spare, I've tried to implement something to store and organize part of the public knowledge around Google App Engine.  
I've coded up this tool that is a sort of mix among Reddit, Delicious and a Cms/Blogging platform.  

Do you want some good tags/categories combo to start with?  

Try with:  
    - [web-frameworks+python](http://www.gaecupboard.com/tag/web-frameworks/python?category=Libraries) in the _Libraries_ category  
    - [reviews](http://www.gaecupboard.com/tag/reviews?category=Articles) in the _Articles_ category  
    - [rants](http://www.gaecupboard.com/tag/rants?category=Articles)  in the _Articles_ category  
    - [java](http://www.gaecupboard.com/tag/java?category=Books)  in the _Books_ category  
    - [pricing](http://www.gaecupboard.com/tag/pricing?category=Articles)  in the _Articles_ category  

You can find me on Stack Overflow as [Systempuntoout](http://stackoverflow.com/search?q=user%3A130929+%5Bgoogle-app-engine%5D) or at the following mail address:  

![test](/images/systempuntooutmail.jpg "mail")
"""



#Views
HTML_MIME_TYPE = "text/html; charset=UTF-8"
DIFF_FROM_UTC_IN_HOURS = +8
THUMBNAIL_WIDTH= 70
THUMBNAIL_HEIGHT= 70
POSTS_PER_PAGE = 10
NAVBAR_CLOUDSIZE = 30
MAIN_CLOUDSIZE = 500
RECENT_POST_NUM = 20
FEATURED_POST_NUM = 30
NO_LIMIT = 10000
MAX_NUMBER_OF_TAGS_FILTERS = 5
MEMCACHE_ENABLED = True #Disable it just for testing
TAGS_BLACK_LIST = ['appengine', 'google-app-engine', 'gae', 'app-engine','ae']
POSTS_PER_SITEMAP = 1000

#Services
DISQUS = "gaecupboard"
CLICKY_ID = '66452880'
ANALYTICS_ID = 'UA-4276204-7'
ADSENSE_ID = 'pub-3296756901484166'
ADSENSE_CHANNEL_ID = '2124691773'
FEED_PROXY = 'http://feeds.feedburner.com/gaecupboard/fb'
FEED_PROXY_USER_AGENT = 'FeedBurner'


#Errors
RELAXING_MESSAGE_ERROR = "..cumulus clouds are white, puffy clouds that look like pieces of floating cotton.. "
GENERIC_ERROR = "Ooooops, it works on my machine. Please try again later."
NOT_FOUND_ERROR = "Not found!"
SERVER_ERROR = "Server problem"
BOTS=['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','Baiduspider','googlebot','Speedy Spider','DotBot']

#Mapping Discovery
AUTO_CONTENT_BY_LINK = {
'http://stackoverflow.com':{
                            'regex':'http://stackoverflow\.com/questions/(\d+).*',
                            'image':'stackoverflow.png',
                            'category':'Questions',
                            'content_block':"""<div id="stacktack-%s"></div>
                            <script type="text/javascript">
                                jQuery(document).stacktack();
                            </script>
                            """
                            
                            },
'http://programmers.stackexchange.com':{
                            'regex':'http://programmers.stackexchange\.com/questions/(\d+).*',
                            'image':'programmers.png',
                            'category':'Questions',
                            'content_block':"""<div id="stacktack-%s"></div>
                            <script type="text/javascript">
                                jQuery(document).ready(function() {
                                jQuery(document).stacktack({site: 'programmers.stackexchange.com'});
                                });
                            </script>                            
                            """
                            },
'http://www.slideshare.net':{
                            'regex':'(.*)',
                            'image':'slideshare.png',
                            'category':'Articles',
                            'content_block':"""
                            <div id="content">
                                <a href="%s"></a>
                            </div>"""
                            },

'http://vimeo.com':{
                            'regex':'(.*)',
                            'image':'vimeo.png',
                            'category':'Videos',
                            'content_block':"""
                            <div id="content">
                                <a href="%s"></a>
                            </div>"""
                            },       
'http://blip.tv':{
                            'regex':'(.*)',
                            'image':'bliptv.png',
                            'category':'Videos',
                            'content_block':"""
                            <div id="content">
                                <a href="%s"></a>
                            </div>"""
                            },  
'http://www.youtube.com':{
                            'regex':'(.*)',
                            'image':'youtube.png',
                            'category':'Videos',
                            'content_block':"""
                            <div id="content">
                                <a href="%s"></a>
                            </div>"""
                            },                          
                            
'https://github.com':{
                            'image':'github.png',
                            'category':'Libraries',
                            },
'https://gist.github.com':{
                            'image':'github.png',
                            'category':'Libraries',
                            },
'https://bitbucket.org':{
                        'image':'bitbucket.png',
                        'category':'Libraries',
                        },
'http://code.google.com':{  'url_paths':['/p'], #different images for different url path on the same domain
                            'image':'googlecode_documentation.png',
                            'image_/p':'googlecode_hosting.png',
                            'category':'Libraries',
                            },
'http://groups.google.com':{
                            'image':'googlegroups.png',
                            'category':'Articles',
                            },
'http://blog.notdot.net':{
                            'image':'notdot.png',
                            'category':'Articles',
                            },
'http://www.reddit.com':{
                            'image':'reddit.png',
                            'category':'Articles',
                            },
'http://googleappengine.blogspot.com':{
                            'image':'blogappengine.png',
                            'category':'Articles',
                            },
'http://news.ycombinator.com':{
                            'image':'hackernews.png',
                            'category':'Articles',
                            },
'http://www.amazon.com':{
                            'regex':'http://www.amazon.com/dp/(.*)/.*',
                            'category':'Books',
                            'content_block':"""
                            <iframe src="http://rcm.amazon.com/e/cm?lt1=_blank&bc1=000000&IS2=1&nou=1&
                              bg1=FFFFFF&fc1=000000&lc1=0000FF&t=syst-20&o=1&p=8&l=as4&m=amazon&f=ifr&
                              ref=ss_til&asins=%s"style="width:120px;height:240px;
                              "scrolling="no"marginwidth="0"marginheight="0"frameborder="0">
                             </iframe>"""
                            },
}

AUTO_CONTENT_BY_CATEGORY = {
'Applications':{
            'content_block':'<iframe id="frame" src="%s"></iframe>'
        }
}

#Bookmarklets

ADMIN_BOOKMARKLET = """
javascript:(function(){var s=window.document.createElement('script');s.setAttribute('src','http://code.jquery.com/jquery-latest.min.js');
window.document.body.appendChild(s);f='http://%s/admin?action=newpost_init&link='+encodeURIComponent(window.location.href)+'&tags='+encodeURIComponent(jQuery.map(jQuery('.post-taglist a,#eow-tags a,.post-info a').not('#edit-tags'),function(x){return encodeURIComponent(x.text)}).join(' '))+'&title='+encodeURIComponent(document.title)+'&description='+encodeURIComponent(''+(window.getSelection?window.getSelection():document.getSelection?document.getSelection():document.selection.createRange().text))+'&';a=function(){location.href=f};if(/Firefox/.test(navigator.userAgent)){setTimeout(a,0)}else{a()}})()
""" % HOST

USER_BOOKMARKLET ="""
javascript:(function(){var s=window.document.createElement('script');s.setAttribute('src','http://code.jquery.com/jquery-latest.min.js');
window.document.body.appendChild(s);f='http://%s/submit?action=submit_init&link='+encodeURIComponent(window.location.href)+'&tags='+encodeURIComponent(jQuery.map(jQuery('.post-taglist a,#eow-tags a,.post-info a').not('#edit-tags'),function(x){return encodeURIComponent(x.text)}).join(' '))+'&title='+encodeURIComponent(document.title)+'&description='+encodeURIComponent(''+(window.getSelection?window.getSelection():document.getSelection?document.getSelection():document.selection.createRange().text))+'&';a=function(){location.href=f};if(/Firefox/.test(navigator.userAgent)){setTimeout(a,0)}else{a()}})()
""" % HOST
