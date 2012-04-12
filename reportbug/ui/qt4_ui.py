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
from reportbug.urlutils import launch_browser
from reportbug.exceptions import NoPackage, NoBugs, NoNetwork, NoReport

DEBIAN_LOGO = "/usr/share/pixmaps/debian-logo.png"


app = None
win = None

def log_message(message, *args):
    if args:
        message %= args
    if win is None:
        print message
    else:
        win.log_message(message)
display_report = log_message
final_message = log_message

def display_failure(message, *args):
    if args:
        message %= args
    sys.stderr.write(message)
    sys.stderr.flush()

def disable_progressbar(func):
    # FIXME: The progressbar is not shown while Python is computing, because
    # Python threads are not compatible with Qt threads.
    def newf(*args, **kwargs):
        win.progressbar(False)
        response = func(*args, **kwargs)
        win.progressbar(True)
        return response
    return newf

def exit_dialog():
    response = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'reportbug',
            'Do you want to exit reportbug?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_()
    if response == QtGui.QMessageBox.Yes:
        sys.exit(0)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(700, 550)
        self.setWindowIcon(QtGui.QIcon(DEBIAN_LOGO))
        self._status = QtGui.QPlainTextEdit(self)
        self._status.setReadOnly(True)
        self._progressbar = QtGui.QProgressBar(self)
        self._progressbar.setRange(0, 0)
        self.progressbar(True)
        self.progressbar(False)
    def log_message(self, message):
        self._status.appendPlainText('\n' + message)

    def resizeEvent(self, event):
        self._status.move(0, self._progressbar.height())
        self._status.resize(self.width(),
                self.height() - self._progressbar.height())
        self._progressbar.resize(self.width(),
                self._progressbar.height())

    def progressbar(self, enable):
        if enable:
            self._progressbar.show()
            self.resizeEvent(None)
        else:
            self._progressbar.hide()
            self.resizeEvent(None)

class YesNo(QtGui.QMessageBox):
    def __init__(self, message, yeshelp, nohelp, default):
        super(YesNo, self).__init__(self.Question, 'reportbug', message)
        self.setModal(True)
        self.setInformativeText('Yes: %s\nNo: %s' % (yeshelp, nohelp))
        self.addButton(self.Yes)
        self.addButton(self.No)
        self.setDefaultButton(self.Yes if default else self.No)

@disable_progressbar
def get_string(prompt, options=None, title=None, empty_ok=False, force_prompt=False,
               default='', completer=None):
    ok = False
    prompt = prompt.replace(' (enter Ctrl+c to exit reportbug without reporting a bug)', '')
    # If you don't like the following line, ask Qt to give us access to
    # QInputDialog.label.setWordWrap()
    prompt = textwrap.fill(prompt)
    while not ok:
        dialog = QtGui.QInputDialog(win)
        dialog.setTextValue(default)
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

class Menu(QtGui.QDialog):
    def __init__(self, parent, title, question, options, prompt, multiple):
        super(Menu, self).__init__(parent)
        self.setModal(True)
        self.resize(600, 500)
        self.setWindowTitle(title or '')
        self._multiple = multiple
        self._selection = []
        self._abort = True

        self._question = QtGui.QLabel(question, self)
        self._options = options
        self._groupbox = QtGui.QGroupBox(self)
        self._groupbox.setLayout(QtGui.QVBoxLayout())
        Widget = QtGui.QCheckBox if multiple else QtGui.QRadioButton
        def on_toggle_generator(key):
            def on_toggle(checked):
                if checked and key not in self._selection:
                    self._selection.append(key)
                elif not checked and key in self._selection:
                    self._selection.remove(key)
            return on_toggle
        if isinstance(options, tuple):
            options = dict(options)
        elif isinstance(options, list):
            options = dict(options)
        for key, description in options.items():
            widget = Widget('%s: %s' % (key, description))
            widget.toggled.connect(on_toggle_generator(key))
            self._groupbox.layout().addWidget(widget)

        self._buttonbox = QtGui.QDialogButtonBox(self)
        self._buttonbox.addButton(self._buttonbox.Ok)
        self._buttonbox.addButton(self._buttonbox.Cancel)
        self._buttonbox.clicked.connect(self._on_button_click)
        self._buttonbox.show()

    def resizeEvent(self, event):
        self._groupbox.move(0, self._question.height())
        self._groupbox.resize(self.width(), self.height() - self._buttonbox.height())
        self._buttonbox.move(self.width() - self._buttonbox.width(),
                self.height() - self._buttonbox.height())

    def exec_(self):
        super(Menu, self).exec_()
        return None if self._abort else self._selection

    def _on_button_click(self, button):
        button = self._buttonbox.standardButton(button)
        if button == self._buttonbox.Cancel:
            exit_dialog()
        else:
            self._abort = False
            self.close()



@disable_progressbar
def menu(question, options, prompt, default=None, title=None, any_ok=False,
         order=None, extras=None, multiple=False, empty_ok=False):
    response = None
    while response is None or (len(response) == 0 and not empty_ok):
        dialog = Menu(win, title, question, options, prompt, multiple)
        response = dialog.exec_()
        if response is None:
            exit_dialog()
            continue
    return response if multiple else response[0]

def select_multiple(par, options, prompt, title=None, order=None, extras=None):
    return menu(par, options, prompt, title=title, order=order, extras=extras,
                multiple=True, empty_ok=False)


@disable_progressbar
def yes_no(message, yeshelp, nohelp, default=True, nowrap=False):
    yesno = YesNo(message=message, yeshelp=yeshelp, nohelp=nohelp,
            default=default)
    yesno.show()
    response = yesno.exec_()
    assert response in (yesno.Yes, yesno.No)
    return response == yesno.Yes

class Bug(QtGui.QDialog):
    class MessageList(QtGui.QWidget):
        def __init__(self, messages, parent=None):
            super(Bug.MessageList, self).__init__(parent)
            self._height = 0
            self._resizing = False
            self._textedits = []
            self.setSizePolicy(QtGui.QSizePolicy(
                    QtGui.QSizePolicy.Expanding,
                    QtGui.QSizePolicy.Expanding))
            for message in messages:
                textedit = QtGui.QPlainTextEdit(self)
                textedit.setPlainText(message)
                textedit.setReadOnly(True)
                self._textedits.append(textedit)
                self.resize(self.width(), self._height + 100000)
                textedit.adjustSize()
                metrics = QtGui.QFontMetrics(textedit.font())
                textedit.resize(textedit.width(),
                        # Number of lines of the document:
                        (textedit.document().documentLayout().documentSize().toSize().height()+3)*
                        # Height of a line:
                        metrics.height())
                textedit.move(0, self._height)
                self._height += textedit.height()
            self.setMinimumHeight(self._height)
            self.resize(self.width(), self._height + 100000)
        def resizeEvent(self, event):
            super(Bug.MessageList, self).resizeEvent(event)
            for textedit in self._textedits:
                textedit.resize(self.width(), textedit.height())
    def __init__(self, bug, parent=None, **kwargs):
        super(Bug, self).__init__(parent)
        self.setModal(True)
        self.resize(600, 500)
        self._bug = bug
        self._kwargs = kwargs
        self._abort = True
        info = debbugs.get_report(int(bug.bug_num), None, **kwargs)

        self._description = QtGui.QLabel('Description:'+info[0].subject, self)
        self._description.show()

        self._scrollarea = QtGui.QScrollArea(self)
        self._scrollarea.setWidget(Bug.MessageList(info[1], self._scrollarea))
        self._scrollarea.setWidgetResizable(True)
        self._scrollarea.show()

        self._buttonbox = QtGui.QDialogButtonBox(self)
        self._button_openbrowser = QtGui.QPushButton('Open in browser',
                self._buttonbox)
        self._buttonbox.addButton(self._button_openbrowser,
                self._buttonbox.ActionRole)
        self._button_reply = QtGui.QPushButton('Reply', self._buttonbox)
        self._buttonbox.addButton(self._button_reply,
                self._buttonbox.ActionRole)
        self._buttonbox.addButton(self._buttonbox.Close)
        self._buttonbox.clicked.connect(self._on_button_click)
        self._buttonbox.show()

    def closeEvent(self, event):
        if self._abort:
            # User closed the window or pressed 'Cancel'
            self.parent()._selected_bug = None
        else:
            # User clicked the 'reply' button
            self._abort = False
            self.parent()._abort = False
            self.parent().close()

    def resizeEvent(self, event):
        (x, y) = (self.width(), self.height()) # shortcuts
        self._description.resize(x, self._description.height())
        self._buttonbox.move(self.width() - self._buttonbox.width(),
                self.height() - self._buttonbox.height())
        self._scrollarea.move(0, self._description.height())
        self._scrollarea.resize(x,
                y - (self._buttonbox.height()+self._description.height()))

    def _on_button_click(self, button):
        standardbutton = self._buttonbox.standardButton(button)
        if standardbutton == self._buttonbox.Close:
            self.close()
        elif button == self._button_openbrowser:
            launch_browser(debbugs.get_report_url(self._kwargs['system'],
                int(self._bug.bug_num), self._kwargs['mirrors'] or None,
                self._kwargs['archived'] or None))
        elif button == self._button_reply:
            self._abort = False
            self.close()


class BugList(QtGui.QDialog):
    class Bug(QtGui.QTreeWidgetItem):
        columns = (
                ('bug_num', 'ID'),
                ('tags', 'Tag'),
                ('package', 'Package'),
                ('subject', 'Description'),
                ('pending', 'Status'),
                ('originator', 'Submitter'),
                ('date', 'Date'),
                ('severity', 'Severity'),
                ('found_versions', 'Versions'),
                ('log_modified', 'Modified date'),
                )
        @classmethod
        def header(cls):
            return [y for x,y in cls.columns]

        def __init__(self, bug):
            list_ = QtCore.QStringList()
            for attr, verbose_name in self.columns:
                value = getattr(bug, attr)
                formatter = ', '.join if isinstance(value, list) else str
                list_.append(formatter(value))
            super(BugList.Bug, self).__init__(list_)

    def __init__(self, parent, reports, bug_kwargs):
        super(BugList, self).__init__(parent)
        self.setModal(True)
        self._abort = True
        self._selected_bug = None
        self._bug_kwargs = bug_kwargs
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
        Bug(self._bugs[bug_num], self, **self._bug_kwargs).show()

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
        print repr(self._abort)
        print repr(self._selected_bug)
        if self._abort: # Should not happen
            exit_dialog()
        elif self._selected_bug is None:
            return None
        else:
            return self._bugs[self._selected_bug]


@disable_progressbar
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
    bug = BugList(win, report, {'mirrors': mirrors, 'http_proxy': http_proxy,
            'archived': archived, 'system': bts}).exec_()
    print repr(bug)
    assert bug is None or isinstance(bug, debbugs.debianbts.Bugreport)
    return bug

class Editor(QtGui.QDialog):
    def __init__(self, parent, message, filename):
        super(Editor, self).__init__(parent)
        self.setModal(True)
        self._abort = True

        self.resize(600, 500)
        self._textedit = QtGui.QPlainTextEdit(self)
        self._textedit.setDocumentTitle(filename)
        self._textedit.setPlainText(message)
        self._buttonbox = QtGui.QDialogButtonBox(self)
        self._buttonbox.addButton(self._buttonbox.Ok)
        self._buttonbox.addButton(self._buttonbox.Cancel)
        self._buttonbox.clicked.connect(self._on_button_click)
        self._buttonbox.show()

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        self._buttonbox.move(self.width() - self._buttonbox.width(),
                self.height() - self._buttonbox.height())
        self._textedit.resize(self.width(),
                self.height() - self._buttonbox.height())

    def _on_button_click(self, button):
        button = self._buttonbox.standardButton(button)
        if button == self._buttonbox.Cancel:
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
        super(Editor, self).exec_()
        assert not self._abort
        return self._textedit.toPlainText()

@disable_progressbar
def spawn_editor(message, filename, editor, charset='utf-8'):
    editor = Editor(win, message, filename)
    new_message = str(editor.exec_())
    return (new_message, message == new_message)

class ButtonList(QtGui.QDialog):
    def __init__(self, parent, msg, ok, help_, title):
        super(ButtonList, self).__init__(parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.setModal(True)
        self._buttons = {}
        self._clicked = None

        def on_click_generator(key):
            def on_click(checked):
                self._clicked = key
                self.close()
            return on_click
        for key in ok:
            button = QtGui.QPushButton(help_[key.lower()])
            self.layout().addWidget(button)
            button.clicked.connect(on_click_generator(key))
            if key != key.lower(): # It is upper-cased
                button.setFocus()
            button.show()
            self._buttons.update({key: button})

    def closeEvent(self, event):
        if self._clicked is None:
            exit_dialog()

    def exec_(self):
        super(ButtonList, self).exec_()
        return self._clicked

@disable_progressbar
def select_options(msg, ok, help=None, allow_numbers=False, nowrap=False,
                   ui=None, title=None):
    response = None
    while response is None:
        response = ButtonList(win, msg, ok, help or {}, title or 'reportbug').exec_()
    return response

def long_message(message, *args, **kwargs):
    log_message(message, *args)

def get_filename(prompt, title=None, force_prompt=False, default=''):
    return str(QtGui.QFileDialog.getOpenFileName(win, title or '', default))

def initialize():
    global app, win
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.progressbar(True)
    return True

def can_input():
    return True
ISATTY = True
