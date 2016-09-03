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
from subprocess import Popen

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
        cmds[cmd]()