import unittest2

from reportbug import utils
from reportbug import debbugs
from reportbug.bugreport import bugreport
from nose.plugins.attrib import attr
import debianbts

class TestBugreport(unittest2.TestCase):

# TODO: differentiate for all possible cases? f.e. sysinfo True/False and then change if 'System Information' in self.text?

    def test_bugreport(self):
        self.body = 'test'
        self.package = 'reportbug'
        self.report = bugreport(package=self.package, body=self.body)
        self.text = self.report.__unicode__()

        self.assertIn(self.body, self.text)
        self.assertIn(self.package, self.text)
        self.assertIn(utils.NEWBIELINE, self.text)

    # verify that for special packages, we don't add the report template
    def test_bts643785(self):
        for package in debbugs.SYSTEMS['debian'].get('specials', {}).keys():
            self.report = bugreport(package=package, mode=utils.MODE_NOVICE)
            self.text = self.report.__unicode__()
            self.assertNotIn(utils.NEWBIELINE, self.text)

    @attr('network') #marking the test as using network
    def test_followup(self):
        self.body = 'test'
        self.package = 'reportbug'
        self.report = bugreport(package=self.package, body=self.body,
                                followup=123456)
        self.text = self.report.__unicode__()

        self.assertIn('Followup-For: Bug #123456', self.text)
        self.assertNotIn('Severity: ', self.text)

        # test also a bugreport instance, and a datatype unconvertible to int
        bug = debianbts.get_status(123456)[0]
        self.report = bugreport(package=self.package, body=self.body,
                                followup=bug)
        self.text = self.report.__unicode__()

        self.assertIn('Followup-For: Bug #123456', self.text)
        self.assertNotIn('Severity: ', self.text)

        with self.assertRaises(TypeError):
            self.report = bugreport(package=self.package, body=self.body,
                                    followup={'123456': 654321})
