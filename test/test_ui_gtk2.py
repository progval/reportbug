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

# These tests were written in the main module,
# moved here to see if they can be interested somehow,
# but to use them, we'd need to find a way to interact
# programmatically with the GTK+ widgets
#def test ():
#    # Write some tests here
#    print get_password ("test")
#    print select_options ('test', 'A', {'a': 'A test'})
#    print get_multiline ('ENTER', empty_ok=True)
#    print get_string ("test")
#    print system ("yes")
#    page = HandleBTSQueryPage (assistant)
#    application.run_once_in_main_thread (page.execute_operation, [('test', (Bug ('#123 [test] [we] we we Reported by: test;' ), Bug ('#123 [test] [we] we we Reported by: test;')))], 'test')
#    return application.get_last_value ()
