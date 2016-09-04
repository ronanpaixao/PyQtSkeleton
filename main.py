#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
<application name>
Copyright ©<year> <author>
Licensed under the terms of the <LICENSE>.

See LICENSE for details.

@author: <author>
"""

from __future__ import division, unicode_literals, print_function

import sys
import os
import os.path as osp
import subprocess
import ctypes
import logging

#%% Setup PyQt's v2 APIs. Must be done before importing PyQt or PySide
import rthook

#%%
from qtpy import QtCore, QtGui, QtWidgets, uic

import six

#%% PyInstaller Utilities
def frozen(filename):
    """Returns the filename for a frozen file (program file which may be
    included inside the executable created by PyInstaller).
    """
    if getattr(sys, 'frozen', False):
        return osp.join(sys._MEIPASS, filename)
    else:
        return filename

#%% I usually need some sort of file/dir opening function
if sys.platform == 'darwin':
    def show_file(path):
        subprocess.Popen(['open', '--', path])
    def open_default_program(path):
        subprocess.Popen(['start', path])
elif sys.platform == 'linux2':
    def show_file(path):
        subprocess.Popen(['xdg-open', '--', path])
    def open_default_program(path):
        subprocess.Popen(['xdg-open', path])
elif sys.platform == 'win32':
    def show_file(path):
        subprocess.Popen(['explorer', '/select,', path])
    open_default_program = os.startfile

#%% Simple thread example (always useful to avoid locking the GUI)
class CallbackThread(QtCore.QThread):
    """Simple threading example.

    The thread executes a callback function. Use self if you want to store
    variables as the thread instance's attributes. It is also useful to use
    arguments as default values. This examples prints after 2 seconds:

    >>> def callback_fcn(self, t=2):
    ...     self.sleep(t)
    ...     print("Thread Finished")
    ...
    >>> thread = CallbackThread()
    >>> thread.callback = callback_fcn
    >>> thread.start()  # Finishes after 2 seconds
    """
    def __init__(self, *args, **kwargs):
        super(CallbackThread, self).__init__(*args, **kwargs)
        self.callback = lambda *args: None
        self.ret = None

    def __del__(self):
        self.wait()

    def run(self):
        self.ret = self.callback(self)

#%% Logging to GUI
class ConsoleWindowLogHandler(logging.Handler, QtCore.QObject):
    log = QtCore.pyqtSignal(str, name="log")
    def __init__(self, parent=None):
        super(ConsoleWindowLogHandler, self).__init__()
        QtCore.QObject.__init__(self, parent)

    def emit(self, logRecord):
        message = unicode(self.format(logRecord))
        self.log.emit(message)

#%%
class WndMain(QtWidgets.QMainWindow):
    ######################
    ### Initialization ###
    ######################
    def __init__(self, *args, **kwargs):
        super(WndMain, self).__init__(*args, **kwargs)
        self.initUI()
        # Logging setup
        consoleHandler = ConsoleWindowLogHandler(self.txtLog)
        logger = logging.getLogger()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        consoleHandler.setFormatter(logger.handlers[0].formatter)
        logger.name = "<app_name>"
        logger.addHandler(consoleHandler)
        consoleHandler.log.connect(self.on_consoleHandler_log)
        self.logger = logger
        # Threading example with new-style connections
        self.thread = CallbackThread(self)
        def callback_fcn(self, t=2):
            self.sleep(t)
            logging.info("Thread finished.")  # Shouldn't translate log msgs
        self.thread.callback = callback_fcn
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.start()

    def initUI(self):
        ui_file = frozen(osp.join('data', 'wndmain.ui'))
        uic.loadUi(ui_file, self)
        self.show()

    @QtCore.pyqtSlot()
    def on_thread_finished(self):
        QtWidgets.QMessageBox.information(self,
                                          self.tr("Information"),
                                          self.tr("Thread finished."))

    @QtCore.pyqtSlot(str)
    def on_consoleHandler_log(self, message):
        self.txtLog.appendPlainText(message)

#%%
if __name__ == '__main__':
    # Properly register window icon
    myappid = u'br.com.dapaixao.pyqtskeleton.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    existing = QtWidgets.qApp.instance()
    if existing:
        app = existing
    else:
        app = QtWidgets.QApplication(sys.argv)
    # Setup internationalization/localization (i18n/l10n)
    translator = QtCore.QTranslator()
    translator.load(frozen(osp.join("data", "main.qm")))
    QtWidgets.qApp.installTranslator(translator)
    wnd = WndMain()
    if existing:
        self = wnd
    else:
        sys.exit(app.exec_())
