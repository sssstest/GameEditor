GameEditor
==========

Supports reading GameMaker and ENIGMA game formats. GMK version 800+ (reading and writing), GMX, GMZ, EGM

git clone GameEditor into your enigma-dev directory and dont rename the directory because its hardcoded. Start the commands in enigma-dev

    python GameEditor/cli.py gamefile.gmx
    python GameEditor/ide.py
    python GameEditor/ide.py gamefile.gmx

The cli is for converting and compiling games on the command line. Writing might write corrupt game files so dont overwrite anything without having a backup.

You can test GML code with the cli using

    python GameEditor/cli.py -c 'show_message("test");game_end();'

That will create a game with 1 room and 1 object and the code in the event create action. On the terminal it will show

    show_message: test

Requirements

You need Python and PyQt4 installed

Windows

http://python.org/download/
http://www.riverbankcomputing.com/software/pyqt/download
