# -*- coding: utf-8 -*-

"""
Tests for utility
"""

import unittest
from app.utility.utils import Pagination,ContentDiscoverer

class PaginationTestCase(unittest.TestCase):
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
        self.assertEquals(ContentDiscoverer("http://stackoverflow.com/questions/6085551").get_id(), '6085551')
        self.assertEquals(ContentDiscoverer("http://www.youtube.com/watch?v=ZAkQJOlcrbI&feature=aso").get_id(), 'ZAkQJOlcrbI')
        self.assertEquals(ContentDiscoverer("http://www.youtube.com/watch?v=tcbpTQXNwac").get_id(), 'tcbpTQXNwac')
       
if __name__ == '__main__':
    unittest.main()
