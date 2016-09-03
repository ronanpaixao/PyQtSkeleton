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

##Planned
* Translation file

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