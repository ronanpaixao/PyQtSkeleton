# PyQtSkeleton
A very basic project to make it easier to jump-start other PyQt/PySide projects

##Included
* This README.md
* .gitignore for Python apps (modified)
* Uses the excellent [qtpy compatibility layer](https://github.com/spyder-ide/qtpy) from the guys that make Spyder IDE
* Selection of PyQt API v2
* Begginning wndmain.ui (dynamically loaded)
* Custom PNG icon template with correct exhibition on taskbar
* Simple callback thread example
* CHANGELOG.md example
* Logging utilities using the `logging` default module
* Simple run.py to execute simple commands (a little like Make). No dependencies.
* PyInstaller spec file to convert whole program into a single .exe file. This spec file includes:
    * Single-file EXE generation
    * Multi-resolution conversion of PNG icon to ICO (depends on Pillow)
    * `data` folder automatic inclusion in executable
    * `frozen()` function to facilitate using frozen data files
    * Exclusion of unused Qt modules (comment if your app uses them)
    * Uses UPX if available
Note: when using some libraries, you'll need setuptools version 19.2, or the EXE generation might fail.
* Translation i18n support through Qt Linguist. Supports translating (and loading) in multiple languages with the `--lang` option, which defaults to the system's language.
* Window position and state saving. Settings are stored in an INI file, which can be used for other program settings.

### Install dependencies

```bash
pip install qtpy
pip install PyInstaller
```

or

```bash
conda install qtpy
pip install PyInstaller
```

## How to use

1. Copy the files to your new project's directory.

2. Change the `README.md` file to reflect your project's characteristics.

3. Rename `main.py` to `<yourproject>.py` and `main.spec` to
`<yourproject>.spec`if you want.

4. Open `<yourproject>.spec` and change the `name` variable to your project's
name. Also change the `main.py` file in the _Analysis_ step to
`<yourproject>.py` like you renamed in the previous step.

5. Open the `<yourproject>.py` file and change the header as you wish,
specially the _application name_, _author_ and _LICENSE_ parts.

6. In the bottom of the file, change the `myappid` variable to match your
project's details. This is used to set your executable's icon separate from
other Python processes in the window manager.

7. Trim the unused parts of the project. The Thread and ConsoleHandler usages
are just examples for useful features.

8. The window and icon files are in the `data` directory. Put application
resources in this directory, so that they will be automatically included when
using PyInstaller. Remember to use the `frozen()` function when using those
resources' filenames.

9. When ready to freeze the app, go to the command line and use:

```
pyinstaller <yourproject>.spec
```

10. Enjoy!

## Troubleshooting

If your script doesn't build with PyInstaller, try one or more of these in the
`<yourproject>.spec` file:

1. Change the `single_file` variable to `False`. This will put all files in a
directory. Looking at the gathered files may help identify missing DLLs.

2. In the `EXE()` call, change `console=False` to `console=True`. After that,
when running the built executable from the command line, it is possible to see
errors and tracebacks that may help find where the problem is.

3. If that's not enough, change `debug=False` to `debug=True`. This will enable
PyInstaller's debug messages which are shown when the program is loading the
script.

Remember to revert these changes when the problem is solved.
