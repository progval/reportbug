""" Unit test for reportbug.ui.gtk2_ui module """

import unittest2

from nose.plugins.attrib import attr

from reportbug import utils
from reportbug.ui import gtk2_ui as ui
import debianbts

class TestUIGTK2(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_bug_class(self):
        bug = debianbts.get_status(415801)[0]

        gtk_bug = ui.Bug(bug)

        self.assertIsNotNone(gtk_bug)
        self.assertEqual(bug.bug_num, gtk_bug.id)
        self.assertEqual(bug.severity, gtk_bug.severity)
        self.assertEqual(bug.package, gtk_bug.package)
        self.assertEqual(bug.originator, gtk_bug.reporter)
        self.assertEqual(bug.date, gtk_bug.date)
        for tag in bug.tags:
            self.assertIn(tag, gtk_bug.tag)

        for item in gtk_bug:
            self.assertIsNotNone(item)
