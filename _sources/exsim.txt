Simulation examples
=====================

These examples have simulation.
    
ledramp
--------------------------

Program:

.. literalinclude:: ../pysimavrgui/examples/sim/ledramp.py

Starting program:

.. runblock:: pycon
    
    >>> from pysimavrgui.examples.sim.ledramp import run_sim
    >>> run_sim(vcdfile='docs/ledramp.vcd', speed=0.1, timeout=0.2, fps=50, visible=0, image_file='docs/ledramp.png')

GUI:

.. image:: ledramp.png    
    
Signals:

.. gtkwave:: docs/ledramp.vcd
    
   
    
LCD
--------------------------

Program:

.. literalinclude:: ../pysimavrgui/examples/sim/lcd.py

Starting program:

.. runblock:: pycon
    
    >>> from pysimavrgui.examples.sim.lcd import run_sim
    >>> run_sim(vcdfile='docs/lcd.vcd', speed=1, timeout=0.2, fps=50, visible=0, image_file='docs/lcd.png')

GUI:

.. image:: lcd.png    
    
Signals:

.. gtkwave:: docs/lcd.vcd
    

  
    
seven segment display
--------------------------

Program:

.. literalinclude:: ../pysimavrgui/examples/sim/sgm7.py

Starting program:

.. runblock:: pycon
    
    >>> from pysimavrgui.examples.sim.sgm7 import run_sim
    >>> run_sim(vcdfile='docs/sgm7.vcd', speed=1, timeout=0.1, fps=50, visible=0, image_file='docs/sgm7.png')

GUI:

.. image:: sgm7.png    
    
Signals:

.. gtkwave:: docs/sgm7.vcd
    

.. include:: links.rst    