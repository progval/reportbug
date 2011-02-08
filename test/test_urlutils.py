import unittest2

from reportbug import urlutils

class TestNetwork(unittest2.TestCase):

    def test_open_url(self):

        page = urlutils.open_url('http://bugs.debian.org/reportbug')
        content = page.read()
        self.assertIsNotNone(page.info().headers)
