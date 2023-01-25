"""
start
====================================================

This is where the magic starts. This runs everytime you
start MA-1.

while True: loop in this script makes sure that the MA-1 is
always alive

"""

# Import CircuitPython libs
import supervisor, time, board, neopixel

# Import Magical Apes global libs
import lib_cp_magicalapes.system as ma_system
import lib_cp_magicalapes.output.display_ssd1306 as ma_display
import lib_cp_magicalapes.output.sound as ma_sound
import lib_cp_magicalapes.utils as ma_utils

# Import MA1 specific libs
# These libraries are configurable in config.py
# Extend, hack, make your own to your herts content
from config import life
ma1_state = __import__(life['state'], globals(), locals(), [], 0)
ma1_emotions = __import__(life['emotions'], globals(), locals(), [], 0)
import ma1.stopwatch as ma1_stopwatch

# Switch off the internal LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=neopixel.RGB)
led.brightness = .1
led[0] = (0, 0, 0)

# system can be used to read the temprature, voltage etc.
system = ma_system.System(board.A3)

# Create the I2C interface for OLED, use any pins you like, we are going with GP0 (SDA) & GP1 (SCL)
# busio.I2C(SCL, SDA)
i2c = system.open_i2c(board.GP11, board.GP10)

# This initialised MA1 specific sensors and state
ma1 = ma1_state.LSTM(i2c)

# Create a I2C display channel
display = ma_display.Display_I2C(128, 64, i2c)
display.contrast(1)

# Initialize buzzer pin
tone = ma_sound.Tone(board.GP1)

# Initialize MA1 emotions
emotions = ma1_emotions.Emotions(display, tone)
# This call is optional, you can make your MA1 startup with anything you like
# eg, a nice tone, some nice text, your custom emotions etc.
emotions.startup()

# Initialize MA1 stopwatch
stopwatch = ma1_stopwatch.Stopwatch(display, tone)

# Keep previous state to compare
pre_state = ma1.state_array

MODE_NORMAL = 0
MODE_LEFT = 1
MODE_RIGHT = 2
MODE_UPSIDE = 3
DELAY = 0.1

# Local variables and constants you can adapt
no_activity_timer = ma_utils.Timer()
break_timer = ma_utils.Timer()
mode = MODE_NORMAL

while True:

    time.sleep(DELAY)

    if system.temp >= 50:
        # must be switched off and move away from heat
        emotions.hot()
        continue

    break_timer.measure()

    # This measures the state of all connected sensors
    ma1.measure()
    
    # Get previous and current states
    dark = ma1.dark
    sound = ma1.sound
    touch = ma1.touch
    picked = ma1.picked
    left = ma1.left
    right = ma1.right
    upside = ma1.upside
    quick_move = ma1.quick_move

    if right[1] == 1:
        mode = MODE_RIGHT
    elif upside[1] == 1:
        mode = MODE_UPSIDE
    else:
        mode = MODE_NORMAL # Normal or left is the same
    
    if mode == MODE_NORMAL:
        if left[1] and no_activity_timer.elapsed > 20:
            emotions.dream()
        elif dark[1] and no_activity_timer.elapsed > 300:
            emotions.sleep()
        elif no_activity_timer.elapsed > 1800:
            emotions.wonder()
        elif no_activity_timer.elapsed > 600:
            emotions.quiet()

        if break_timer.elapsed > 3600:
            # Time to prompt for a break
            # But only if its not dreaming and its not dark / night time
            if not left[1] and not dark[1]:
                emotions.need_a_break()
                break_timer.reset()

        # Only continue if the state has changed
        if not ma1.state_changed:
            no_activity_timer.measure()
            continue

        no_activity_timer.reset()

        if quick_move[1]:
            emotions.dizzy()
        elif picked[1] and touch[1]:
            emotions.content()
        elif picked[1]:
            emotions.happy()
        elif touch[1]:
            emotions.good()
        else:
            stopwatch.reset()
            emotions.neutral()
            
    elif mode == MODE_RIGHT:
        stopwatch.show()
    elif mode == MODE_UPSIDE:
        display.rotation = 2
        display.fill(0)
        display.text('Busy', 30, 20, 1, size=3)
        display.show()
