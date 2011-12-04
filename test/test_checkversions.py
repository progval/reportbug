import unittest2

from reportbug import checkversions
from nose.plugins.attrib import attr

class TestCheckversions(unittest2.TestCase):

    def test_compare_versions(self):
        # <current, upstream>
        # 1 upstream newer than current
        # 0 same version or upsteam none
        # -1 current newer than upstream
        self.assertEqual(checkversions.compare_versions('1.2.3', '1.2.4'), 1)

        self.assertEqual(checkversions.compare_versions('123', None), 0)
        self.assertEqual(checkversions.compare_versions('1.2.3', '1.2.3'), 0)
        self.assertEqual(checkversions.compare_versions(None, None), 0)
        self.assertEqual(checkversions.compare_versions('', '1.2.3'), 0)

        self.assertEqual(checkversions.compare_versions('1.2.4', '1.2.3'), -1)

    def test_later_version(self):
        # mock the test_compare_Versions() test

        self.assertEqual(checkversions.later_version('1.2.3', '1.2.4'), '1.2.4')

        self.assertEqual(checkversions.later_version('123', None), '123')
        self.assertEqual(checkversions.later_version('1.2.3', '1.2.3'), '1.2.3')
        self.assertIsNone(checkversions.later_version(None, None))
        self.assertEqual(checkversions.later_version('', '1.2.3'), '')

        self.assertEqual(checkversions.later_version('1.2.4', '1.2.3'), '1.2.4')

class TestVersionAvailable(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_bts642032(self):
        vers = checkversions.get_versions_available('reportbug', 60)
        # check stable version is lower than unstable
        chk = checkversions.compare_versions(vers['stable'], vers['unstable'])
        self.assertEqual(chk, 1)

    @attr('network') #marking the test as using network
    def test_bts649649(self):
        # checking for non-existing package should not generate a traceback
        vers = checkversions.get_versions_available('blablabla', 60)
        self.assertEqual(vers, {})
