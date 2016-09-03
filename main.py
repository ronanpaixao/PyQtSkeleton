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

#%% Setup PyQt's v2 APIs. Must be done before importing PyQt or PySide
import rthook

#%%
from qtpy import QtCore, QtGui, QtWidgets, uic

import six

#%%
def frozen(filename):
    """Returns the filename for a frozen file (program file which may be
    included inside the executable created by PyInstaller).
    """
    if getattr(sys, 'frozen', False):
        return osp.join(sys._MEIPASS, 'wndmain.ui')
    else:
        return 'wndmain.ui'

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

#%%
class WndMain(QtWidgets.QMainWindow):
    ######################
    ### Initialization ###
    ######################
    def __init__(self, *args, **kwargs):
        super(WndMain, self).__init__(*args, **kwargs)
        self.initUI()
        # Threading example with new-style connections
        self.thread = CallbackThread(self)
        def callback_fcn(self, t=2):
            self.sleep(t)
            print("Thread Finished")
        self.thread.callback = callback_fcn
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.start()

    def initUI(self):
        ui_file = frozen('wndmain.ui')
        uic.loadUi(ui_file, self)
        self.show()

    @QtCore.pyqtSlot()
    def on_thread_finished(self):
        QtWidgets.QMessageBox.information(self,
                                          self.tr("Information"),
                                          self.tr("Thread finished."))


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
    wnd = WndMain()
    if existing:
        self = wnd
    else:
        sys.exit(app.exec_())