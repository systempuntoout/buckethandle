from datetime import datetime, timedelta
from google.appengine.api import memcache
import unicodedata
import re
import logging


def memcached(key, cache_time, key_suffix_calc_func=None, namespace=None):
    """
     Cache to memcache
    """
    def wrap(func):
        def cached_func(*args, **kw):
            key_with_suffix = key

            if key_suffix_calc_func:
                key_suffix = key_suffix_calc_func(*args, **kw)
                if key_suffix:
                    key_with_suffix = '%s:%s' % (key, key_suffix)

            value = memcache.get(key_with_suffix, namespace)
            if not value:
                value = func(*args, **kw)
                memcache.set(key_with_suffix, value, cache_time, namespace)
            return value
        return cached_func
    return wrap

def slugify(value):
    """ Slugify a string, to make it URL friendly. """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+','-',value)

def generate_key_name():
    return now().strftime("%Y%m%d%H%M%S")

def now():
    return datetime.utcnow() + timedelta(hours =+ 8)

class Pagination(object):
    def __init__(self, total, page, pagesize):
        self.total = int(total)
        self.page = int(page)
        self.pagesize = int(pagesize)
        self.total_pages = 0 if self.total==0 else 1 if (self.total / self.pagesize == 0) else (self.total / self.pagesize) \
                             if (self.total % self.pagesize == 0) else (self.total / self.pagesize) + 1
        self.separator = "..."

    def has_more_entries(self):
        return (self.page < self.total_pages)
    def has_previous_entries(self):
        return (self.page > 1)
    def get_pretty_pagination(self):
        """
            Return a list of int representing page index like:
            [1, -1 , 6 ,  7 , 8 , -1 , 20]
            -1 is where separator will be placed
        """
        pagination = []
        if self.total_pages == 1:
            return pagination
        pagination.append(1)
        if self.page > 2:
            if ( self.total_pages > 3 and self.page > 3 ):
                pagination.append(-1)
            if self.page == self.total_pages and self.total_pages > 3 :
                pagination.append(self.page - 2)
            pagination.append(self.page - 1)
        if self.page != 1 and self.page != self.total_pages :
            pagination.append(self.page)
        if self.page < self.total_pages - 1 :
            pagination.append(self.page + 1)
            if  self.page == 1 and self.total_pages > 3:
                pagination.append(self.page + 2)
            if ( self.total_pages > 3 and self.page < self.total_pages - 2 ):
                pagination.append(-1)
        pagination.append(self.total_pages)
        return pagination

def get_predefined_image_link(link, category):
    if link.startswith('http://stackoverflow.com'):
        return '/images/predefined/stackoverflow.png'
    if link.startswith('http://www.youtube.com'):
        return '/images/predefined/youtube.png'
    if link.startswith('https://github.com'):
        return '/images/predefined/github.png'
    if link.startswith('http://code.google.com'):
        return '/images/predefined/googlecode.png'
    #Categories
    return '/images/predefined/%s.png' % category.lower()


class ContentDiscoverer():
    def __init__(self,link):
        self.link = link
    def get_id(self):
        try:
            if self.link.startswith('http://stackoverflow.com'):
                re_so = re.compile('http://stackoverflow\.com/questions/(\d+)/.*')
                return re_so.match(self.link).group(1)
            elif self.link.startswith('http://www.youtube.com'):
                re_yt = re.compile('http://www\.youtube\.com/watch\?v=([^&]*)')
                return re_yt.match(self.link).group(1)    
            else: return None
        except:
            return None    
        
    def get_content_block(self):
        if self.link.startswith('http://stackoverflow.com'):
            id = self.get_id()
            if id:
                return """<div id="stacktack-%s"></div>""" % id
            else:
                return ""
        elif self.link.startswith('http://www.youtube.com'):  
            id = self.get_id()
            if id:
                return """
                <div id="youtube">
                    <iframe width="560" height="349" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>
                </div>""" % id
            else:
                return ""
        else: return ""
            
    