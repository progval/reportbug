import unittest2

from reportbug import checkbuildd
from nose.plugins.attrib import attr

class TestCheckbuildd(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_check_built(self):
        built = checkbuildd.check_built('gkrellm', 60)
        self.assertTrue(built)
