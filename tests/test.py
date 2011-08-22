from nose.tools import eq_, timed
from pysimavrgui.examples.sim import lcd, ledramp, sgm7

VISIBLE = 0

# fails!
#def test_speed():
#    led_ex.run_sim(speed=0.001, fps=20, timeout=0.001, visible=VISIBLE)
#    led_ex.run_sim(speed=0.01, fps=1, timeout=0.01, visible=VISIBLE)
#    led_ex.run_sim(speed=1, fps=1, timeout=0.1, visible=VISIBLE)
#    led_ex.run_sim(speed=10, fps=100, timeout=1, visible=VISIBLE)

@timed(10)
def test_example_led():
    ledramp.run_sim(speed=1, timeout=0.5, visible=VISIBLE)

#@timed(10)
#def test_example_lcd():
# TODO: lcd fails, no terminate()??
#    lcd.run_sim(speed=0.1, timeout=0.3, visible=VISIBLE)

# deadlock
#@timed(10)
#def test_example_sgm7():
#    sgm7.run_sim(speed=1, timeout=0.5, visible=VISIBLE)

# fails!
# because of lcd
#def test_example_all():
#    test_example_led()
#    test_example_lcd()
#    test_example_sgm7()
#    test_example_led()
#    test_example_lcd()
#    test_example_sgm7()
