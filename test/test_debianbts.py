import unittest2

from nose.plugins.attrib import attr

from reportbug import utils
from reportbug import debianbts

class TestDebianbts(unittest2.TestCase):

    def test_get_tags(self):

        # for each severity, for each mode
        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])

        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch'])

        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])

        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental', 'wheezy'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental', 'wheezy', 'security'])


class TestInfofunc(unittest2.TestCase):

    def test_dpkg_infofunc(self):
        info = debianbts.dpkg_infofunc()
        self.assertIn('Architecture:', info)

    def test_debian_infofunc(self):
        info = debianbts.debian_infofunc()
        self.assertIn('Architecture:', info)

    def test_ubuntu_infofunc(self):
        info = debianbts.ubuntu_infofunc()
        self.assertIn('Architecture:', info)

    def test_generic_infofunc(self):
        info = debianbts.generic_infofunc()
        self.assertIn('Architecture:', info)

class TestMiscFunctions(unittest2.TestCase):

    def test_yn_bool(self):
        self.assertEqual(debianbts.yn_bool(None), 'no')
        self.assertEqual(debianbts.yn_bool('no'), 'no')
        self.assertEqual(debianbts.yn_bool('yes'), 'yes')
        self.assertEqual(debianbts.yn_bool('dummy string'), 'yes')

    def test_convert_severity(self):

        # lists of bts systems, severity and the expected value in return
        sevs = [('debbugs', 'critical', 'critical'),
                ('debbugs', 'non-critical', 'normal'),
                (None, 'dummy', 'dummy'),
                ('gnats', 'important', 'serious'),
                ('gnats', 'dummy', 'dummy')]

        for type, severity, value in sevs:
            self.assertEqual(debianbts.convert_severity(severity, type), value)


class TestGetReports(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_get_cgi_reports(self):

        data = debianbts.get_cgi_reports('reportbug', timeout=60)
        self.assertGreater(data[0], 0)


    @attr('network') #marking the test as using network
    def test_get_reports(self):

        data = debianbts.get_reports('reportbug', timeout=60)
        self.assertGreater(data[0], 0)

    @attr('network') #marking the test as using network
    def test_get_report(self):

        data = debianbts.get_report(415801, 120)
        self.assertEqual(data[0],
               '#415801: reportbug: add support for SOAP interface to BTS')

class TestUrlFunctions(unittest2.TestCase):

    def test_cgi_report_url(self):

        self.assertEqual(debianbts.cgi_report_url('debian', 123),
                         'http://bugs.debian.org/cgi-bin/bugreport.cgi?' +
                             'bug=123&archived=False&mbox=no')
        self.assertIsNone(debianbts.cgi_report_url('default', 123))

    def test_cgi_package_url(self):

        self.assertEqual(debianbts.cgi_package_url('debian', 'reportbug'),
                         'http://bugs.debian.org/cgi-bin/pkgreport.cgi?' +
                             'archived=no&pkg=reportbug&repeatmerged=yes')
        self.assertEqual(debianbts.cgi_package_url
                         ('debian', 'reportbug', source=True),
                         'http://bugs.debian.org/cgi-bin/pkgreport.cgi?src=' +
                             'reportbug&archived=no&repeatmerged=yes')
        self.assertEqual(debianbts.cgi_package_url
                         ('debian', 'reportbug', version='5.0'),
                         'http://bugs.debian.org/cgi-bin/pkgreport.cgi?archi' +
                         'ved=no&version=5.0&pkg=reportbug&repeatmerged=yes')


    def test_get_package_url(self):

        self.assertEqual(debianbts.get_package_url('debian', 'reportbug'),
                         'http://bugs.debian.org/cgi-bin/pkgreport.cgi?archi' +
                         'ved=no&pkg=reportbug&repeatmerged=yes')

    def test_get_report_url(self):

        self.assertEqual(debianbts.get_report_url('debian', 123),
                         'http://bugs.debian.org/cgi-bin/bugreport.cgi?' +
                         'bug=123&archived=False&mbox=no')
