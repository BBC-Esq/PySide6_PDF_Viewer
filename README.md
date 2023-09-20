# PySide6 PDF Viewer
Simple PDF viewer made with PySide6.  Scoured the Internet for days and finally found a way to do it so here you go.  If you want one using PyQt instead of Pyside, check out my other repository.<br>

This repository has two viewers, one based on javascript and the other using the Chromium engine that is part of Pyside6.  I'll let you decide who has the better implementation.

# Installation
> First, make sure you're running [Python 3.10+](https://www.python.org/downloads/release/python-31011/)
  
* Download the latest releast and unzip the folder to somewhere on your computer.  Then, open the folder containing my repository files, create a command prompt, and create a virtual environment:
```
python -m venv .
```
* Activate the virtual environment:
```
.\Scripts\activate
```
* Upgrade pip
```
python -m pip install --upgrade pip
```

* Install Dependencies
```
pip install PySide6==6.5.2
```
* Unzip Javascript Files
> You must unzip the folder within the ZIP file to the same exact directory where the scripts are located.
# Run Program
  * For Javascript Version
```
python pyside6_pdfviewer_js.py
```
  * For Non-Javascript Version
```
python pyside6_pdfviewer.py
```

## If you found it useful please star so more people can find the repository!
