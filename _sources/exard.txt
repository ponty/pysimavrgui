Arduino simulator
=====================

How to use it:
 - start arduino software
 - compile a sketch, the firmware will be saved in temporary directory
 - start the arduino simulator example: ```python -m pysimavrgui.examples.sim.arduino```
   The name of the sketch is displayed on the GUI.
 - after recompiling in arduino select 'reload' on simulator GUI
    
    
LCD sketch
--------------------------

.. literalinclude:: ../pysimavrgui/examples/arduino/lcd.pde

.. program-screenshot:: python -m pysimavrgui.examples.sim.arduino -c pysimavrgui/examples/arduino/lcd.pde
    :prompt:
    :wait: 1

LED sketch
--------------------------

.. literalinclude:: ../pysimavrgui/examples/arduino/led.pde

.. program-screenshot:: python -m pysimavrgui.examples.sim.arduino -c pysimavrgui/examples/arduino/led.pde
    :prompt:
    :wait: 1

print sketch
--------------------------

.. literalinclude:: ../pysimavrgui/examples/arduino/print.pde

.. program-screenshot:: python -m pysimavrgui.examples.sim.arduino -c pysimavrgui/examples/arduino/print.pde
    :prompt:
    :wait: 1

    
.. include:: links.rst    