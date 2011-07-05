from datetime import datetime, timedelta
from google.appengine.api import memcache
from app.config.settings import *
import unicodedata
import re
import logging
import time
import urlparse
import math


def memcached(key, cache_time, key_suffix_calc_func=None, namespace=None):
    """
     Cache to memcache
    """
    def wrap(func):
        def cached_func(*args, **kw):
            if MEMCACHE_ENABLED:
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
            else:
                value = func(*args, **kw)
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

def get_base_link(link):
    if link:
        parsed_link = urlparse.urlparse(link)
        return parsed_link.scheme + "://" + parsed_link.netloc
    else:
        return None

class Pagination(object):
    def __init__(self, total, page, pagesize):
        self.total = int(total)
        self.page = int(page)
        self.pagesize = int(pagesize)
        self.total_pages = 0 if self.total==0 else 1 if (self.total / self.pagesize == 0) else (self.total / self.pagesize) \
                             if (self.total % self.pagesize == 0) else (self.total / self.pagesize) + 1

    def has_more_entries(self):
        return (self.page < self.total_pages)
    def has_previous_entries(self):
        return (self.page > 1)

def inverse_microsecond_str(): 
    """gives string of 8 characters from ascii 23 to 'z' which sorts in reverse temporal order"""
    t = datetime.now()
    inv_us = int(1e16 - (time.mktime(t.timetuple()) * 1e6 + t.microsecond)) #no y2k for >100 yrs
    base_100_str = ""
    while inv_us:
        digit, inv_us = inv_us % 100, inv_us / 100
        base_100_str = chr(23 + digit) + base_100_str
    return base_100_str

def get_predefined_image_link(link = None, category = None):
    #By link
    if link:
        base_link = get_base_link(link)
        if base_link in AUTO_CONTENT_BY_LINK and 'image' in AUTO_CONTENT_BY_LINK[base_link] :
            if 'url_paths' in AUTO_CONTENT_BY_LINK[base_link]:
                for path in AUTO_CONTENT_BY_LINK[base_link]['url_paths']:
                    if link.startswith(base_link+path):
                        return '/images/predefined/%s' % AUTO_CONTENT_BY_LINK[base_link]['image_%s' % path]
            return '/images/predefined/%s' % AUTO_CONTENT_BY_LINK[base_link]['image']
    #By category
    if category:
        return '/images/predefined/%s.png' % category.lower()
    return '/images/predefined/predefined_nocategory.png' 


class ContentDiscoverer():
    def __init__(self,link, category = ''):
        self.link = link
        self.category = category
    def get_id(self):
        base_link = get_base_link(self.link)
        try:
            if base_link in AUTO_CONTENT_BY_LINK and 'regex' in AUTO_CONTENT_BY_LINK[base_link] :
                re_tmp = re.compile(AUTO_CONTENT_BY_LINK[base_link]['regex'])
                return re_tmp.match(self.link).group(1)
        except:
            return None    
        
    def get_content_block(self):
        base_link = get_base_link(self.link)
        if base_link in AUTO_CONTENT_BY_LINK and 'content_block' in AUTO_CONTENT_BY_LINK[base_link] :
            return AUTO_CONTENT_BY_LINK[base_link]['content_block'] % self.get_id()
        if self.category in AUTO_CONTENT_BY_CATEGORY and 'content_block' in AUTO_CONTENT_BY_CATEGORY[self.category]:
            return AUTO_CONTENT_BY_CATEGORY[self.category]['content_block'] % self.link
        return ""
            
def get_tag_weight(occurrencies, max_occurrencies):
    try:
        return int(math.log(occurrencies)/math.log(max_occurrencies) * (5-1)+1)
    except:
        return 0