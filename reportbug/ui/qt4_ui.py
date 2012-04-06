# a graphical (GTK+) user interface
#   Written by Luca Bruno <lethalman88@gmail.com>
#   Based on gnome-reportbug work done by Philipp Kern <pkern@debian.org>
#   Copyright (C) 2006 Philipp Kern
#   Copyright (C) 2008-2009 Luca Bruno
#
# This program is freely distributable per the following license:
#
##  Permission to use, copy, modify, and distribute this software and its
##  documentation for any purpose and without fee is hereby granted,
##  provided that the above copyright notice appears in all copies and that
##  both that copyright notice and this permission notice appear in
##  supporting documentation.
##
##  I DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL I
##  BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
##  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
##  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
##  SOFTWARE.

import sys

from PyQt4 import QtCore, QtGui

DEBIAN_LOGO = "/usr/share/pixmaps/debian-logo.png"


app = None

def log_message(message, *args):
    if args:
        message %= args
    print message

def display_failure(message, *args):
    if args:
        message %= args
    sys.stderr.write(message)
    sys.stderr.flush()

def exit_dialog():
    response = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'reportbug',
            'Do you want to exit reportbug?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_()
    if response == QtGui.QMessageBox.Yes:
        sys.exit(0)

class YesNo(QtGui.QMessageBox):
    def __init__(self, message, yeshelp, nohelp, default):
        super(YesNo, self).__init__(self.Question, 'reportbug', message)
        self.setInformativeText('Yes: %s\nNo: %s' % (yeshelp, nohelp))
        self.addButton(self.Yes)
        self.addButton(self.No)
        self.setDefaultButton(self.Yes if default else self.No)

def get_string(prompt, options=None, title=None, empty_ok=False, force_prompt=False,
               default='', completer=None):
    ok = False
    while not ok:
        response, status = QtGui.QInputDialog.getText(None, title or '', prompt)
        if status:
            if response == '' and not empty_ok:
                print '-'*50
                QtGui.QMessageBox.warning(None, 'reportbug',
                        'Empty answer is not allowed.')
            else:
                ok = True
        else:
            exit_dialog()
    return response

def menu(question, options, prompt, default=None, title=None, any_ok=False,
         order=None, extras=None, multiple=False, empty_ok=False):
    if multiple:
        raise NotImplemented('Multiple choice menu has not been implemented')
    response = []
    while len(response) == 0:
        response, status = QtGui.QInputDialog.getItem(None, title or '',
                question, [y for x,y in options], 0, False)
        if not status:
            exit_dialog()
            continue
    return str(response)


def yes_no(message, yeshelp, nohelp, default=True, nowrap=False):
    yesno = YesNo(message=message, yeshelp=yeshelp, nohelp=nohelp,
            default=default)
    yesno.show()
    response = yesno.exec_()
    assert response in (yesno.Yes, yesno.No)
    return response == yesno.Yes


def initialize():
    global app
    app = QtGui.QApplication(sys.argv)
    return True

def can_input():
    return True
ISATTY = True
