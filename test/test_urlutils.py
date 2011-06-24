import unittest2

from nose.plugins.attrib import attr

from reportbug import urlutils

class TestNetwork(unittest2.TestCase):

    @attr('network') #mark the test as using network
    def test_open_url(self):

        page = urlutils.open_url('http://bugs.debian.org/reportbug')
        content = page.read()
        self.assertIsNotNone(page.info().headers)
