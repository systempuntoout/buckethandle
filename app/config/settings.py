# -*- coding: utf-8 -*-
#Meta
CMS_NAME = u"GAEcupboard"
AUTHOR_NAME = u"systempuntoout"
SLOGAN = u"Ingredients for your Google App Engine recipes"
DESCRIPTION = u"""Google App Engine knowledge base"""             
META_DESCRIPTION = u"GAEcupboard - Ingredients for your Google App Engine recipes"
META_KEYWORDS = u"Gae appengine Google App Engine  libraries tutorial videos projects stackoverflow "
CATEGORIES = [u"Libraries",u"Articles", u"Questions", u"Videos", u"Applications",u"Books"]
MAIL_ADMIN = u"systempuntoout@gmail.com"
ABOUT =u"""
This is a five days hack project made after a meniscus surgery ([buckethandle](http://www.leadingmd.com/patientEd/assets/buckethandle_tear.gif "buckethandle")).  
Having some time to spare, I've tried to implement something to store and organize all the public knowledge around Google App Engine.  
I've coded this tool that is a sort of mix between Reddit, a blogging platform and Delicious.  
I love Delicious but there is too much noise and duplicates in the tons of links bookmarked every day, I like reddit and it's fantastic for the hottest news but I miss a tagging feature  a là delicious or Stack Overflow.  
The data is now collected through a semi-automatic process and hopefully with your help.  

This tool is a work in progress, so expect errors and other nasty things;
I've kept the code pretty configurable for other sites and topics and I'm planning to open-source it if it will gain some interest and traction.  


Feedback at this address:  
![test](/images/systempuntooutmail.jpg "mail")
"""



#Views
HTML_MIME_TYPE = "text/html; charset=UTF-8"
THUMBNAIL_WIDTH= 70
THUMBNAIL_HEIGHT= 70
POSTS_PER_PAGE = 15
NAVBAR_CLOUDSIZE = 30
RECENT_POST_NUM = 20
FEATURED_POST_NUM = 10
NO_LIMIT = 10000
MAX_NUMBER_OF_TAGS_FILTERS = 5
MEMCACHE_ENABLED = True #Disable it just for testing
TAGS_BLACK_LIST = ['appengine', 'google-app-engine', 'gae', 'app-engine','ae']

#Services
DISQUS = "gaecupboard"
CLICKY_ID = None
ANALYTICS_ID = 'UA-4276204-7'

#Errors
RELAXING_MESSAGE_ERROR = "..cumulus clouds are white, puffy clouds that look like pieces of floating cotton.. "
GENERIC_ERROR = "Ooooops, it works on my machine. Please try again later."
NOT_FOUND_ERROR = "Not found!"
SERVER_ERROR = "Server problem"

#Mapping Discovery
AUTO_CONTENT_BY_LINK = {
'http://stackoverflow.com':{
                            'regex':'http://stackoverflow\.com/questions/(\d+).*',
                            'image':'stackoverflow.png',
                            'category':'Questions',
                            'content_block':"""<div id="stacktack-%s"></div>"""
                            
                            },
'http://www.youtube.com':{
                            'regex':'http://www\.youtube\.com/watch\?v=([^&]*)',
                            'image':'youtube.png',
                            'category':'Videos',
                            'content_block':"""
                            <div id="youtube">
                                <iframe width="560" height="349" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>
                            </div>"""
                            },
'https://github.com':{
                            'image':'github.png',
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
                            }
}

AUTO_CONTENT_BY_CATEGORY = {
'Applications':{
            'content_block':'<iframe id="frame" src="%s"></iframe>'
        }
}