Simple GUI elements for AVR_ and arduino_ simulation.
Programmed in python_, based on pygame_. 
Simavr_ is used for simulation. 

Links:
 * home: https://github.com/ponty/pysimavrgui
 * documentation: http://ponty.github.com/pysimavrgui
 
Features:
 - designed to use with pysimavr_ (simavr_ wrapper)
 - arduino_ simulator included
 - maximum speed can be real-time
 - speed control
 - audio backend: PyAudio_
 - graphic backend: PyGame_ (SDL_ wrapper)
 
Known problems:
 - Python 3 is not supported
 - tested only on linux
 - real-time sleep() is used in simavr_, so speed control is far from perfect
 - occasional crash by firmware reload  
 - poor sound quality

Installation
============

General
--------

 * install python_
 * install pip_
 * install PyGame_ 
 * install PyAudio_ (optional)
 * install pysimavr_ 
 * install the program::

    # as root
    pip install pysimavrgui


Ubuntu
----------
::

    sudo apt-get install python-pip
    sudo apt-get install python-pygame
    sudo apt-get install python-pyaudio
    
    # pysimavr
    sudo apt-get install swig
    sudo apt-get install python-dev
    sudo apt-get install gcc
    sudo apt-get install libelf-dev
    sudo pip install pysimavr    

    # for arduino
    sudo apt-get install scons
    sudo apt-get install arduino
    
    sudo pip install pysimavrgui

Uninstall
----------

::

    # as root
    pip uninstall pysimavrgui


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _simavr: http://gitorious.org/simavr
.. _pygame: http://pygame.org/
.. _pyaudio: http://people.csail.mit.edu/hubert/pyaudio/
.. _SDL: http://www.libsdl.org/
.. _pysimavr: https://github.com/ponty/pysimavr
.. _AVR: http://en.wikipedia.org/wiki/Atmel_AVR