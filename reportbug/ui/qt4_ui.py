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
import textwrap

from PyQt4 import QtCore, QtGui

from reportbug import debbugs
from reportbug.exceptions import NoPackage, NoBugs, NoNetwork, NoReport

DEBIAN_LOGO = "/usr/share/pixmaps/debian-logo.png"


app = None
win = None

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

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(DEBIAN_LOGO))

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
    # If you don't like the following line, ask Qt to give us access to
    # QInputDialog.label.setWordWrap()
    prompt = textwrap.fill(prompt)
    while not ok:
        dialog = QtGui.QInputDialog(win)
        dialog.setWindowTitle(title or '')
        dialog.setLabelText(prompt)
        if dialog.exec_():
            response = dialog.textValue()
            if response == '' and not empty_ok:
                QtGui.QMessageBox.warning(None, 'reportbug',
                        'Empty answer is not allowed.')
            else:
                ok = True
        else:
            exit_dialog()
    return str(response)

def menu(question, options, prompt, default=None, title=None, any_ok=False,
         order=None, extras=None, multiple=False, empty_ok=False):
    if multiple:
        raise NotImplemented('Multiple choice menu has not been implemented')
    response = []
    while len(response) == 0:
        response, status = QtGui.QInputDialog.getItem(win, title or '',
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

class Bug(QtGui.QDialog):
    def __init__(self, bug, parent=None):
        super(Bug, self).__init__(parent)
        self._bug = bug
        self._label = QtGui.QLabel(repr(bug), self)
        # TODO: implement this

    def closeEvent(self, event):
        self.parent()._selected_bug = None

class BugList(QtGui.QDialog):
    class Bug(QtGui.QTreeWidgetItem):
        columns = {
                'bug_num': 'ID',
                'package': 'Package',
                'pending': 'Status',
                'date': 'Date',
                }
        @classmethod
        def header(cls):
            return cls.columns.values()

        def __init__(self, bug):
            list_ = QtCore.QStringList()
            for attr in self.columns:
                list_.append(str(getattr(bug, attr)))
            super(BugList.Bug, self).__init__(list_)

    def __init__(self, parent, reports):
        super(BugList, self).__init__(parent)
        self._abort = True
        self._selected_bug = None
        self.resize(600, 500)
        self._tree = QtGui.QTreeWidget(self)
        self._tree.setColumnCount(len(self.Bug.header()))
        self._tree.setHeaderLabels(self.Bug.header())
        self._bugs = {}
        for category, bugs in reports:
            self._bugs.update(dict([(x.bug_num, x) for x in bugs]))
            category_widget = QtGui.QTreeWidgetItem(self._tree, [category])
            category_widget.setFirstColumnSpanned(True)
            category_widget.addChildren([self.Bug(x) for x in bugs])
        self._tree.itemActivated.connect(self._on_bug_click)

        self._question = QtGui.QLabel('Do you want to report a new bug?', self)
        self._buttonbox = QtGui.QDialogButtonBox(self)
        self._buttonbox.addButton(self._buttonbox.Yes)
        self._buttonbox.addButton(self._buttonbox.No)
        self._buttonbox.clicked.connect(self._on_button_click)
        self._question.show()
        self._buttonbox.show()

    def resizeEvent(self, event):
        super(BugList, self).resizeEvent(event)
        self._buttonbox.move(self.width() - self._buttonbox.width(),
                self.height() - self._buttonbox.height())
        self._question.move(0, self.height() -
                (self._question.height() + self._buttonbox.height())/2)
        self._tree.resize(self.width(),
                self.height() - self._buttonbox.height())

    def _on_bug_click(self, item, column):
        if self._selected_bug is not None: # user double-clicked fast
            return
        try:
            bug_num = int(item.data(0, QtCore.Qt.DisplayRole).toString())
        except ValueError: # Clicked a root item
            return
        self._selected_bug = bug_num
        Bug(self._bugs[bug_num], self).show()

    def _on_button_click(self, button):
        button = self._buttonbox.standardButton(button)
        if button == self._buttonbox.No:
            exit_dialog()
        else:
            self._abort = False
            self.close()

    def closeEvent(self, event):
        if self._abort: # User closed the window
            exit_dialog()
        else: # Programmatically closing the window
            pass

    def exec_(self):
        super(BugList, self).exec_()
        if self._abort: # Should not happen
            exit_dialog()
        elif self._selected_bug is None:
            return None
        else:
            return self._bugs[self._selected_bug]


def handle_bts_query(package, bts, timeout, mirrors=None, http_proxy="",
                     queryonly=False, screen=None, title="", archived='no',
                     source=False, version=None, mbox=False, buglist=None,
                     mbox_reader_cmd=None, latest_first=False):
    sysinfo = debbugs.SYSTEMS[bts]
    root = sysinfo.get('btsroot')
    if not root:
        return

    if isinstance(package, basestring):
        pkgname = package
        if source:
            pkgname += ' (source)'

        progress_label = 'Querying %s bug tracking system for reports on %s' % (debbugs.SYSTEMS[bts]['name'], pkgname)
    else:
        progress_label = 'Querying %s bug tracking system for reports %s' % (debbugs.SYSTEMS[bts]['name'], ' '.join([str(x) for x in package]))


    try:
        (count, sectitle, hierarchy) = debbugs.get_reports(
            package, timeout, bts, mirrors=mirrors, version=version,
            http_proxy=http_proxy, archived=archived, source=source)

        if not count:
            if hierarchy == None:
                raise NoPackage
            else:
                raise NoBugs
        else:
            if count > 1:
                sectitle = '%d bug reports found' % (count,)
            else:
                sectitle = 'One bug report found'

            report = []
            for category, bugs in hierarchy:
                buglist = [x for x in bugs]
                # XXX: this needs to be fixed in debianbts; Bugreport are
                # not sortable (on bug_num) - see #639458
                sorted(buglist, reverse=latest_first)
                report.append((category, buglist))

    except (IOError, NoNetwork):
        display_failure("Unable to connect to %s BTS." % sysinfo['name'])
    except NoPackage:
        display_failure('No record of this package found.')
        raise NoPackage

    if report == []:
        raise NoReport

    # We don't do "return str(BugList(report).exec_())" because it fails
    # with: "RuntimeError: underlying C/C++ object has been deleted"
    bug = BugList(win, report).exec_()
    assert bug is None or isinstance(bug, debbugs.debianbts.Bugreport)
    return bug

def long_message(message, *args, **kwargs):
    # TODO: implement this
    pass


def initialize():
    global app, win
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    return True

def can_input():
    return True
ISATTY = True
