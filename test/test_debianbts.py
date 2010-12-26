import unittest2

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

        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_ADVANCED).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])

        self.assertItemsEqual(debianbts.get_tags('critical', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('grave', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('serious', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('important', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('does-not-build', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('normal', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('non-critical', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('minor', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])
        self.assertItemsEqual(debianbts.get_tags('wishlist', utils.MODE_EXPERT).keys(), ['sid', 'lenny', 'l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'squeeze', 'experimental'])


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
