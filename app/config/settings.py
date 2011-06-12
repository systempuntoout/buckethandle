# -*- coding: utf-8 -*-
#Meta
CMS_NAME = u"GAE_cupboard"
AUTHOR_NAME = u"systempuntoout"
SLOGAN = u"Ingredients for your Google App Engine recipes"
DESCRIPTION = u"""Google App Engine Hot stuff"""             
META_DESCRIPTION = "GAEcupboard - Ingredients for your Google App Engine recipes"
META_KEYWORDS = "Gae appengine Google App Engine  libraries tutorial videos projects stackoverflow "
CATEGORIES = ["Libraries", "Questions", "Tutorials", "Videos", "Applications","Articles","Books"]
ABOUT =u"""
This is a five days hack project made after a meniscus surgery ([buckethandle](http://www.leadingmd.com/patientEd/assets/buckethandle_tear.gif "buckethandle")).  
Being forced to rest and having some time to spare, I've tried to implement something useful to store and organize all the public knowledge around Google App Engine.  
I've coded this tool that is a sort of mix between a blogging platform and Delicious; what I dislike about delicious is that there is too much noise and duplicates in the tons of links bookmarked every day.  
What I dislike about blog platforms is that they lack a drill-down tag exploring feature a là delicious or Stack Overflow.  
I still have to think an easy way to collect all the data, I'm planning to code a smart bookmarklet that should help me in this task.  
This tool is a work in progress, so expect errors and other nasty things.  

[Source code on Github](http://github.com/systempuntoout/buckethandle "github")

![test](/images/systempuntooutmail.jpg "mail")
"""

#Views
HTML_MIME_TYPE = "text/html; charset=UTF-8"
THUMBNAIL_WIDTH= 70
THUMBNAIL_HEIGHT= 70
POSTS_PER_PAGE = 15
NAVBAR_CLOUDSIZE = 30
RECENT_POST_NUM = 10
NO_LIMIT = 10000
MAX_NUMBER_OF_TAGS_USING_INDEXES = 5
MAX_NUMBER_OF_TAGS_FILTERS = 5

#Services
DISQUS = "firsttestblog"
CLICKY_ID = None
ANALYTICS_ID = None

#Errors
RELAXING_MESSAGE_ERROR = "..cumulus clouds are white, puffy clouds that look like pieces of floating cotton.. "
GENERIC_ERROR = "Ooooops, it works on my machine. Please try again later."
NOT_FOUND_ERROR = "Not found!"
SERVER_ERROR = "Server problem"

