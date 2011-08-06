# -*- coding: utf-8 -*-
# pyso.py
#
# Copyright (C) 2010 Jonathon Watney
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""
pyso.py - Python Stack Overflow library, aka a love letter to @frankythebadcop.
patched for Google App Engine
"""
import gzip
import time
import urllib
import urllib2
import app.lib.simplejson as json 
from google.appengine.api import urlfetch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__version__ = "0.1"
__author__ = "Jonathon Watney <jonathonwatney@gmail.com>"

_question_orders = ("activity", "views", "creation", "votes")
_answer_orders = ("activity", "views", "creation", "votes")
_comment_orders = ("creation", "votes")
_user_orders = ("reputation", "creation", "name")
_tag_badge_orders = ("popular", "activity", "name")


class APIError(Exception):
    """Raised when an error occurs."""
    def __init__(self, url, code, message):
        self.url = url
        self.code = code
        self.message = message


class APISite(object):
    """Provides a way to fetch data from an Stack Overflow API site."""
    def __init__(self, name, version="1.0", api_key="", page_size=100):
        if not name.startswith("http://"):
            name = "http://" + name

        self._name = name
        self._version = version
        self._api_key = api_key
        self._page_size = page_size
        self._start_page = 1

    def __repr__(self):
        return (self._name, self._version, self._api_key)

    def fetch(self, path, results_key, **url_params):
        """
        Fetches all the results for a given path where path is the API URL path.
        results_key is the key of the results list. If url_params is given it's
        key/value pairs are used to build the API query string.
        """
        base_url = "%s/%s/%s" % (self._name, self._version, path)
        params = {
            "key": self._api_key,
            "pagesize": self._page_size,
            "page": self._start_page
            }

        params.update(url_params)

        while True:
            query = urllib.urlencode(params)
            url = "%s?%s" % (base_url, query)
            data = self._get_response_data(url)
            response = json.loads(data)
            count = 0

            if "error" in response:
                error = response["error"]
                code = error["Code"]
                message = error["Message"]

                raise APIError(url, code, message)

            if results_key:
                results = response[results_key]
            else:
                results = response

            if len(results) < 1:
                break

            for result in results:
                yield result

            if len(results) < params["pagesize"]:
                break

            params["page"] += 1

    def _get_response_data(self, url):
        """Gets the response encoded as a string."""
        response = urlfetch.fetch(url,  headers = {'User-Agent': 'GAEcupboard'}, deadline = 10, method = urlfetch.GET)
        return response.content


_site = APISite("api.stackoverflow.com")

def install_site(site):
    """Installs site to use as the default API site."""
    global _site
    _site = site

# Miscellaneous and utility site functions.
def get_sites():
    """Returns a list of all the sites in the Stack Exchange Network."""
    return _site.fetch("sites", "api_sites")

def get_stats():
    """Gets various system statistics."""
    return next(_site.fetch("stats", "statistics"))

def get_errors(id):
    """Simulates an error given its code."""
    return _site.fetch("errors/%s" % id, None)

def get_all_badges():
    """Gets all badges, in alphabetical order."""
    return _site.fetch("badges", "badges")

def get_all_standard_badges():
    """Gets all standard, non-tag-based, badges in alphabetical order."""
    return _site.fetch("badges/name", "badges")

def get_all_tag_badges():
    """Gets all tag-based badges in alphabetical order."""
    return _site.fetch("badges/tags", "badges")

def get_badges(ids, start_date=None, end_date=None):
    """Gets the users that have been awarded the badges identified in ids."""
    path = "badges/%s" % __join(ids)
    params = __translate(locals().copy(), _tag_badge_orders)

    return _site.fetch(path, "badges", **params)

def get_tags(name_contains=None, start_date=None, end_date=None):
    """Gets the tags on all questions, along with their usage counts."""
    params = __translate(locals().copy(), _tag_badge_orders)

    return _site.fetch("tags", "tags", **params)

# Question, answer and post functions.
def get_comments(ids, order_by=None, start_date=None, end_date=None):
    """Gets comments by ids."""
    path = "comments/%s" % __join(ids)
    params = __translate(locals().copy(), _comment_orders)

    return _site.fetch(path, "comments", **params)

def get_posts_comments(ids, order_by=None, start_date=None, end_date=None):
    """Gets the comments associated with a set of posts (questions/answers)."""
    path = "posts/%s/comments" % __join(ids)
    params = __translate(locals().copy(), _comment_orders)

    return _site.fetch(path, "comments", **params)

def get_posts_revisions(ids, start_date=None, end_date=None):
    """Gets the post history revisions for a set of posts."""
    path = "revisions/%s" % __join(ids)
    params = __translate(locals().copy())

    return _site.fetch(path, "revisions", **params)

def get_posts_revision(ids, revision_id, start_date=None, end_date=None):
    """Get a specific post revision."""
    path = "revisions/%s/%s" % (__join(ids), revision_id)
    params = __translate(locals().copy())

    return _site.fetch(path, "revisions", **params)

def get_all_questions(order_by=None, tags=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets question summary information."""
    path = "questions"
    orders = ("activity", "votes", "creation", "featured", "hot", "week", "month")
    params = __translate(locals().copy(), orders)

    return _site.fetch(path, "questions", **params)

def get_all_unanswered_questions(order_by=None, tags=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets questions that have no upvoted answers."""
    path = "questions"
    params = __translate(locals().copy(), ("votes", "creation"))

    return _site.fetch(path, "questions", **params)

def get_question(question_id, body=False, comments=False, start_date=None, end_date=None):
    """Get the question with the given question_id."""
    return (get_questions([question_id], body, comments, start_date, end_date)).next()

def get_questions(ids, order_by=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets the set questions identified in ids."""
    path = "questions/%s" % __join(ids)
    params = __translate(locals().copy(), _question_orders)

    return _site.fetch(path, "questions", **params)

def get_questions_answers(ids, order_by=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets any answers to the questions in ids."""
    path = "questions/%s/answers" % __join(ids)
    params = __translate(locals().copy(), _question_orders)

    return _site.fetch(path, "answers", **params)

def get_questions_comments(ids, order_by=None, start_date=None, end_date=None):
    """Gets the comments associated with a set of questions."""
    path = "questions/%s/comments" % __join(ids)
    params = __translate(locals().copy(), _comment_orders)

    return _site.fetch(path, "comments", **params)

def get_questions_timeline(ids, start_date=None, end_date=None):
    """Get the timelines for the given ids."""
    path = "questions/%s/timeline" % __join(ids)
    params = __translate(locals().copy())

    return _site.fetch(path, "post_timelines", **params)

def get_answers(ids, order_by=None, body=False, start_date=None, end_date=None):
    """Gets the set of answers enumerated in ids."""
    path = "answers/%s" % __join(ids)
    params = __translate(locals().copy(), _answer_orders)

    return _site.fetch(path, "answers", **params)

def get_answers_comments(ids, order_by=None, start_date=None, end_date=None):
    """Gets the comments associated with a set of answers."""
    path = "answers/%s" % __join(ids)
    params = __translate(locals().copy(), _comment_orders)

    return _site.fetch(path, "comments", **params)

# User based fucntions.
def get_all_users(name_contains=None, order_by=None, start_date=None, end_date=None):
    """Gets user summary information."""
    path = "users"
    params = __translate(locals().copy(), _user_orders)

    if name_contains:
        params["filter"] = name_contains

    return _site.fetch(path, "users", **params)

def get_user(user_id):
    """Gets a user by user_id."""
    return next(get_users([user_id]))

def get_users(ids, order_by=None):
    """Gets summary information for a set of users."""
    path = "users/%s" % __join(ids)
    params = __translate(locals().copy(), _user_orders)

    return _site.fetch(path, "users", **params)

def get_users_questions(ids, order_by=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets question summary information for a set of users."""
    path = "users/%s/questions" % __join(ids)
    params = __translate(locals().copy(), _question_orders)

    return _site.fetch(path, "questions", **params)

def get_users_answers(ids, order_by=None, body=False, comments=False):
    """Gets answer summary information for a set of users."""
    path = "users/%s/answers" % __join(ids)
    params = __translate(locals().copy(), _answer_orders)

    return _site.fetch(path, "answers", **params)

def get_users_comments(ids, mentioned_user_id=None, order_by=None, start_date=None, end_date=None):
    """Gets the comments that a set of users have made."""
    path = "users/%s/comments" % __join(ids)
    params = __translate(locals().copy(), _comment_orders)

    if mentioned_user_id:
        path += "/%s" % mentioned_user_id

    return _site.fetch(path, "comments", **params)

def get_users_timelines(ids, start_date=None, end_date=None):
    """Gets actions a set of users have performed."""
    path = "users/%s/timeline" % __join(ids)
    params = __translate(locals().copy())

    return _site.fetch(path, "user_timelines", **params)

def get_user_reputation_changes(ids, start_date=None, end_date=None):
    """Gets information on reputation changes for a set of users."""
    path = "users/%s/reputation" % __join(ids)
    params = __translate(locals().copy())

    return _site.fetch(path, "rep_changes", **params)

def get_users_mentions(ids, order_by=None, start_date=None, end_date=None):
    """Gets comments that are directed at a set of users."""
    path = "users/%s/mentioned" % __join(ids)
    params = __translate(locals().copy(), ("creation", "name"))

    return _site.fetch(path, "comments", **params)

def get_users_badges(ids):
    """Gets the badges that have been awarded to a set of users."""
    path = "users/%s/badges" % __join(ids)

    return _site.fetch(path, "badges")

def get_users_tags(ids, order_by=None):
    """Gets the tags that a set of users has participated in."""
    path = "users/%s/tags" % __join(ids)
    params = __translate(locals().copy(), ("popular", "activity", "name"))

    return _site.fetch(path, "tags", **params)

def get_users_favorites(ids, order_by=None, body=False, comments=False, start_date=None, end_date=None):
    """Gets summary information for the questions that have been favorited by a set of users."""
    path = "users/%s/favorites" % __join(ids)
    params = __translate(locals().copy(), _question_orders)

    return _site.fetch(path, "questions", **params)

def get_all_moderators(name_contains=None, start_date=None, end_date=None):
    """Gets all the moderators on this site."""
    path = "users/moderators"
    params = __translate(locals().copy(), _user_orders)

    return _site.fetch(path, "users", **params)

def __join(ids):
    """Joins a sequence of ids into a semicolon delimited string."""
    return ";".join((str(id) for id in ids))

def __translate(kwargs, orders=[]):
    """Translates function kwargs into URL params."""
    params = dict()

    for key, value in kwargs.items():
        if key == "order_by" and value in orders:
            params["sort"] = value
        elif key == "start_date" and value:
            params["fromdate"] = int(time.mktime(value.timetuple()))
        elif key == "end_date" and value:
            params["todate"] = int(time.mktime(value.timetuple()))
        elif key == "body" and value:
            params["body"] = "true"
        elif key == "answers" and value:
            params["answers"] = "true"
        elif key == "comments" and value:
            params["comments"] = "true"
        elif key == "tags" and value:
            params["tagged"] = ";".join(value)
        elif key == "name_contains" and value:
            params["filter"] = value
        elif key == "title_contains" and value:
            params["filter"] = value

    return params
