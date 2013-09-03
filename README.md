GameEditor
==========

Supports reading GameMaker and ENIGMA game formats
GMK version 800+ (reading and writing)
GMX
GMZ
EGM

git clone GameEditor into your enigma-dev directory and dont rename the directory because its hardcoded
the start the commands in enigma-dev
python GameEditor/cli.py gamefile.gmx
python GameEditor/ide.py
python GameEditor/ide.py gamefile.gmx

The cli is for converting and compiling games on the command line
Wrinting will might write corrupt game files so dont overwrite anything without having a backup

You can test GML code with the cli using
python GameEditor/cli.py -c 'show_message("test");game_end();'
That will create a game with 1 room and 1 object and the code in the event create action. On the terminal it will show
show_message: test

Requirements
Linux and OS X
You need Python 2.7 and PyQt4 installed

Windows
Install Python 2.7 and PyQt4 for Python 2.7
http://python.org/download/
http://www.riverbankcomputing.com/software/pyqt/download

x86
http://python.org/ftp/python/2.7.5/python-2.7.5.msi
http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.3/PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x32.exe
x64
http://python.org/ftp/python/2.7.5/python-2.7.5.amd64.msi
http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.3/PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x64.exe


