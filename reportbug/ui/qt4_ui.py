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

class Dialog(QtGui.QDialog):
    """QDialog with some extra features."""
    OPEN = 0
    CANCELLED = 1
    CONFIRMED = 2
    def __init__(self, title):
        super(Dialog, self).__init__()
        self._title = title
        if title:
            self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(DEBIAN_LOGO))

    def _add_buttonbox(self):
        self._buttonbox = QtGui.QDialogButtonBox(self)
        self._buttonbox.addButton(self._buttonbox.Ok)
        self._buttonbox.addButton(self._buttonbox.Close)
        self._buttonbox.clicked.connect(self._on_click)
        self._buttonbox.show()

    def resizeEvent(self, event):
        if self.height() < self.min_height:
            self.resize(self.width(), self.min_height)
        if self.width() < self.min_width:
            self.resize(self.min_width, self.height())
        if self.width() < 500:
            self.resize(500, self.height())
        self.resize_widgets()

    @property
    def min_height(self):
        """The minimum height of the window."""
        return 0

    @property
    def min_width(self):
        """The minimum width of the window."""
        return 0

    def _on_click(self, button):
        button = self._buttonbox.standardButton(button)
        if button == self._buttonbox.Close:
            self.closeEvent()
        elif button == self._buttonbox.Ok:
            self._on_confirm()

    def closeEvent(self, event=None):
        # TODO: "confirm exit" dialog
        self.close()
        if self._state == self.OPEN: # Don't close reportbug if user validated
                                     # his input.
            self._state = self.CANCELLED
            sys.exit(0)

    def resize_widgets(self):
        """Method called when we should resize our widgets."""
        # Move the QButtonBox to the bottom right corner:
        self._buttonbox.move(self.width() - self._buttonbox.width(),
                self.height() - self._buttonbox.height())

class Prompt(Dialog):
    def __init__(self, title, default, empty_ok):
        super(Prompt, self).__init__(title)
        self._empty_ok = empty_ok
        self._lineedit = QtGui.QLineEdit(self)
        if default:
            self._lineedit.setText(default)
        self._lineedit.setFocus()
        self._lineedit.returnPressed.connect(self._on_confirm)
        self._state = self.OPEN
        self._add_buttonbox()

    @property
    def min_height(self):
        return super(Prompt, self).min_height + self._lineedit.height() + \
                self._buttonbox.height()

    def resize_widgets(self):
        # Make the QLineEdit as large as the window:
        self._lineedit.resize(self.width(), self._lineedit.height())
        super(Prompt, self).resize_widgets()

    def show(self):
        self._lineedit.show()
        self._buttonbox.show()
        super(Prompt, self).show()
    
    def _on_confirm(self):
        if self._lineedit.text() == '' and not self._empty_ok:
            self._messagebox = QtGui.QMessageBox.warning(self,
                    self._title or 'reportbug',
                    'Empty answer is not allowed')
        else:
            self._state = self.CONFIRMED
            self.close()
            # app.exec_() will now end and release control to the main loop

    @property
    def response(self):
        assert self._state != self.OPEN
        return self._lineedit.text() if self._state == self.CONFIRMED else None

class Menu(Dialog):
    def __init__(self, title, question, options, prompt, multiple, empty_ok):
        super(Menu, self).__init__(title)
        self._empty_ok = empty_ok
        self._question = QtGui.QLabel(question, self)
        self._question.setWordWrap(True)
        self._groupbox = QtGui.QGroupBox(prompt, self)
        self._groupbox.setLayout(QtGui.QVBoxLayout())
        button_class = QtGui.QCheckBox if multiple else QtGui.QRadioButton
        self._buttons = dict([(x, button_class(y)) for x,y in options])
        assert len(self._buttons) > 1
        self._buttons.values()[0].setFocus()
        for button in self._buttons.values():
            self._groupbox.layout().addWidget(button)
        self._add_buttonbox()

    @property
    def min_height(self):
        return super(Menu, self).min_height + self._question.height() + \
                self._groupbox.height()

    def resize_widgets(self):
        self._question.resize(self.width(), self._question.height())
        self._groupbox.move(0, self._question.height())
        super(Menu, self).resize_widgets()

    def show(self):
        self._question.show()
        self._groupbox.show()
        super(Dialog, self).show()

    def _on_confirm(self):
        if len(self.response) == 0 and not self._empty_ok:
            message = 'You have to select at least one item' if multiple else \
                    'You have to select an item.'
            self._messagebox = QtGui.QMessageBox.warning(self,
                    self._title or 'reportbug', message)
        else:
            self._state = self.CONFIRMED
            self.close()
            # app.exec_() will now end and release control to the main loop

    @property
    def response(self):
        return [x for x,y in self._buttons.items() if y.isChecked()]


def get_string(prompt, options=None, title=None, empty_ok=False, force_prompt=False,
               default='', completer=None):
    global app
    assert app is not None
    # TODO: honor other arguments
    dialog = Prompt(title=title, default=default, empty_ok=empty_ok)
    dialog.show()
    app.exec_()
    response = dialog.response
    assert empty_ok or response
    return response

def menu(question, options, prompt, default=None, title=None, any_ok=False,
         order=None, extras=None, multiple=False, empty_ok=False):
    menu = Menu(title=title, question=question, options=options, prompt=prompt,
            multiple=multiple, empty_ok=empty_ok)
    menu.show()
    app.exec_()
    response = menu.response
    assert not multiple or len(response) <= 1
    assert empty_ok or len(response) >= 1
    return response if multiple else response[0]


def initialize():
    global app
    app = QtGui.QApplication(sys.argv)
    return True

def can_input():
    return True
ISATTY = True
