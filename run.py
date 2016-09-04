#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
<application name>
Copyright ©<year> <author>
Licensed under the terms of the <LICENSE>.

See LICENSE for details.

@author: <author>
"""
# Imports
from __future__ import unicode_literals, print_function

import sys
import os
import os.path as osp
import argparse
import inspect
from subprocess import Popen, call

#%% Commands
def cmd_designer():
    "Launch Qt Designer"
    exe = osp.join(sys.exec_prefix, "Library", "bin", "designer")
    Popen(exe)

def cmd_assistant():
    "Launch Qt Assistant"
    exe = osp.join(sys.exec_prefix, "Library", "bin", "assistant")
    Popen(exe)

def cmd_linguist():
    "Launch Qt Linguist"
    exe = osp.join(sys.exec_prefix, "Library", "bin", "linguist")
    Popen(exe)

def cmd_pyinstaller():
    "Run PyInstaller with spec file"
    call(["pyinstaller", "main.spec"])

def cmd_translate(lang=None):
    """Translate applications with Qt Linguist
        Optional argument:
            --lang LANG - Language to create/translate [defaults to system language]"""
#    from IPython import embed; embed()
    from qtpy import PYQT4, PYQT5, PYSIDE, QtCore
    if lang is None:
        lang = QtCore.QLocale.system().name()
    if PYQT4:
        pylupdate = "pylupdate4"
    elif PYQT5:
        pylupdate = "pylupdate5"
    elif PYSIDE:
        pylupdate = "pylupdate"
    exe = [osp.join(sys.exec_prefix, "Library", "bin", pylupdate)]
    for r, d, fs in os.walk("."):
        for f in fs:
            if (f.split(".")[-1].lower() in ["py", "ui", "pyw"]):
                print(osp.join(r, f))
                exe.append(osp.join(r, f))
    tsfile = "main_{}.ts".format(lang)
    qmfile = "main_{}.qm".format(lang)
    exe.extend(["-ts", tsfile])
    print(*exe)
    call(exe)
    exe = osp.join(sys.exec_prefix, "Library", "bin", "linguist")
    call([exe, tsfile])
    exe = osp.join(sys.exec_prefix, "Library", "bin", "lrelease")
    call([exe, tsfile, "-qm", osp.join("data", qmfile)])

#%% Execution
if __name__ == "__main__":
    cmds = {}
    max_len = 0
    for name, obj in locals().items():
        if name.startswith('cmd_'):
            cmds[name[4:]] = obj
            max_len = max(max_len, len(name)-4)
    epilog = ("Available commands:\n    " +
              "\n    ".join(["{n:{width}}: {o.__doc__}"
              .format(n=k, o=v, width=max_len)
              for k, v in cmds.items()]))

    formatter = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(description="Utility to run utilities.",
                                     formatter_class=formatter,
                                     epilog=epilog)
    parser.add_argument("command", nargs="+", help="Command to execute")
    cmd_args = {}
    for cmd, fcn in cmds.items():
        try:  # PY2
            args = inspect.getargspec(fcn).args
        except AttributeError:  # PY3
            args = [parameter.name for parameter
                    in inspect.signature(fcn).parameters.values()
                    if parameter.kind == parameter.POSITIONAL_OR_KEYWORD]
        cmd_args[cmd] = args
        for arg in args:
            parser.add_argument("--" + arg)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(-1)
    for cmd in args.command:
        if cmd not in cmds:
            print("Invalid command: {}\n\n{}".format(cmd, epilog))
            sys.exit(-2)
    for cmd in args.command:
        cmds[cmd](**{arg: getattr(args, arg) for arg in cmd_args[cmd] if arg in args})
