# -*- coding: utf-8 -*-

"""
Tests for utility
"""

import unittest
from app.utility.utils import Pagination,ContentDiscoverer

class PaginationTestCase(unittest.TestCase):
    def test_get_pretty_pagination(self):
        self.assertEquals(Pagination(10,1,30).get_pretty_pagination(), [])
        self.assertEquals(Pagination(40,1,30).get_pretty_pagination(), [1,2])
        self.assertEquals(Pagination(100,1,10).get_pretty_pagination(), [1, 2, 3, -1, 10])
        self.assertEquals(Pagination(100,2,10).get_pretty_pagination(), [1, 2, 3, -1, 10])
        self.assertEquals(Pagination(100,3,10).get_pretty_pagination(), [1, 2, 3, 4, -1, 10])
        self.assertEquals(Pagination(100,4,10).get_pretty_pagination(), [1, -1, 3, 4, 5, -1, 10])
        self.assertEquals(Pagination(100,5,10).get_pretty_pagination(), [1, -1, 4, 5, 6, -1, 10])
        self.assertEquals(Pagination(100,6,10).get_pretty_pagination(), [1, -1, 5, 6, 7, -1, 10])
        self.assertEquals(Pagination(100,7,10).get_pretty_pagination(), [1, -1, 6, 7, 8, -1, 10])
        self.assertEquals(Pagination(100,8,10).get_pretty_pagination(), [1, -1, 7, 8, 9, 10])
        self.assertEquals(Pagination(100,9,10).get_pretty_pagination(), [1, -1, 8, 9 , 10])
        self.assertEquals(Pagination(100,10,10).get_pretty_pagination(), [1, -1, 8, 9 , 10])
        
    def test_total_pages(self):
        self.assertEquals(Pagination(0,10,10).total_pages, 0)
        self.assertEquals(Pagination(9,1,10).total_pages, 1)
        self.assertEquals(Pagination(10,1,10).total_pages, 1)
        self.assertEquals(Pagination(11,1,10).total_pages, 2)
        self.assertEquals(Pagination(19,1,10).total_pages, 2)
        self.assertEquals(Pagination(20,1,10).total_pages, 2)
        self.assertEquals(Pagination(21,1,10).total_pages, 3)


class ContentDiscovererCase(unittest.TestCase):
    def test_discovery(self):
        self.assertEquals(ContentDiscoverer("http://stackoverflow.com/questions/6085551/iis-7-5-self-signed").get_id(), '6085551')
        self.assertEquals(ContentDiscoverer("http://www.youtube.com/watch?v=ZAkQJOlcrbI&feature=aso").get_id(), 'ZAkQJOlcrbI')
        self.assertEquals(ContentDiscoverer("http://www.youtube.com/watch?v=tcbpTQXNwac").get_id(), 'tcbpTQXNwac')
       
if __name__ == '__main__':
    unittest.main()
