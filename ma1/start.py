"""
start
====================================================

This is where the magic starts. This runs everytime you
start MA-1.

while True: loop in this script makes sure that the MA-1 is
always alive

"""

# Import CircuitPython libs
import os, supervisor, time, board, neopixel

# Import Magical Apes global libs
import lib_cp_magicalapes.system as ma_system
import lib_cp_magicalapes.output.display_ssd1306 as ma_display
import lib_cp_magicalapes.output.sound as ma_sound
import lib_cp_magicalapes.output.lights as ma_lights
import lib_cp_magicalapes.utils as ma_utils

# Import MA1 specific libs
# These libraries are configurable in settings.toml file
# Extend, hack, make your own to your hearts content
ma1_state = __import__(os.getenv('state_module'), globals(), locals(), [], 0)
ma1_emotions = __import__(os.getenv('emotions_module'), globals(), locals(), [], 0)

# Read settings.toml / create constants
BRIGHTNESS_DAY = os.getenv('brightness_day')
BRIGHTNESS_NIGHT = os.getenv('brightness_night')
MODE_NORMAL = 0
MODE_LEFT = 1
MODE_RIGHT = 2
MODE_UPSIDE = 3
DELAY = 0.1

# Switch off the internal LED
pixels = ma_lights.Pixel(board.GP16, n_pixels=1)
pixels.clear()

# This is needed since CircuitPython displayio does not release i2c pin during soft reboots
ma_display.release()

# system can be used to read the chip temperature, voltage etc.
system = ma_system.System(vsys = board.A3)

# Create the I2C interface for OLED, use any pins you like, we are going with GP13 (SDA) & GP12 (SCL)
# busio.I2C(SCL, SDA)
# Do not increase i2c frequency above 800_000 otherwise some parts like touch sensor might not respond
i2c = system.open_i2c(board.GP13, board.GP12, freq=800_000)

# This initialises MA1 specific sensors and state
ma1 = ma1_state.LSTM(i2c)

# Create a I2C display channel
display = ma_display.Display_I2C(128, 64, i2c)
display.contrast(1)

# Initialize buzzer pin
tone = ma_sound.Tone(board.GP3)

# Initialize MA1 emotions
emotions = ma1_emotions.Emotions(display, tone)
# This call is optional, you can make your MA1 startup with anything you like
# eg, a nice tone, some nice text, your custom emotions etc.
emotions.startup()

# Keep previous state to compare
pre_state = ma1.state_array

# Local variables and constants you can adapt
screen_timer = ma_utils.Timer()
no_activity_timer = ma_utils.Timer()
break_timer = ma_utils.Timer()
god_mode_timer = ma_utils.Timer()
mode = MODE_NORMAL
env_data = None
screen = 0
sleeping = False
polluted = False

while True:

    time.sleep(DELAY)

    if system.temp >= 50:
        # must be switched off and move away from heat
        emotions.hot()
        continue

    # This measures the state of all connected sensors
    ma1.measure()

    # Get previous and current states
    dark = ma1.dark
    touch = ma1.touch
    picked = ma1.picked
    left = ma1.left
    right = ma1.right
    upside = ma1.upside
    quick_move = ma1.quick_move
    polluted = ma1.polluted

    if dark[1]:
        emotions.brightness = BRIGHTNESS_NIGHT
    else:
        emotions.brightness = BRIGHTNESS_DAY

    if left[1] == 1:
        mode = MODE_LEFT
    elif right[1] == 1:
        mode = MODE_RIGHT
    elif upside[1] == 1:
        mode = MODE_UPSIDE
    else:
        mode = MODE_NORMAL

    env_data = ma1.env_data
    if env_data:
        if mode == MODE_RIGHT:
            display.rotation = 3
            screen_timer.measure()
            if screen_timer.elapsed >= 5:
                screen = 1 - screen # toggle screen
                screen_timer.reset()
            emotions.polluted(env_data, show_data=True, screen=screen)
            # Turned right, no need to evaluate the rest
            continue
        else:
            screen_timer.reset()
            screen = 0 # so we always start with the first screen on tilt
            if polluted[1]:
                # critical levels, do not evaluate the rest
                display.rotation = 0
                emotions.polluted(env_data)
                continue


    if mode == MODE_NORMAL:
        display.rotation = 0
        sleeping = False
        god_mode_timer.reset()
        break_timer.measure()

        if dark[1] and no_activity_timer.elapsed > 3600:
            emotions.sleep()
        elif no_activity_timer.elapsed > 1800:
            emotions.wonder()
        elif no_activity_timer.elapsed > 600:
            emotions.quiet()

        if break_timer.elapsed > 3600:
            break_timer.reset()
            # Time to prompt for a break
            # But only if its not dark / night time
            if not dark[1]:
                emotions.need_a_break()

        # Only continue if the state has changed
        if not ma1.state_changed:
            no_activity_timer.measure()
            continue

        no_activity_timer.reset()

        if quick_move[1]:
            emotions.afraid(repeat=30)
        elif picked[1] and touch[1]:
            emotions.happy(anim=True)
        elif picked[1]:
            if not picked[0]: # only if the previous state was not picked
                emotions.eyes_up(anim=True)
            else:
                emotions.eyes_up()
        elif touch[1]:
            emotions.touch()
        else:
            emotions.neutral()

    elif mode == MODE_LEFT:
        god_mode_timer.reset()
        if sleeping:
            display.rotation = 0
            emotions.sleep()
        elif touch[1]:
            sleeping = True
            emotions.eyes_down()
    elif mode == MODE_RIGHT:
        god_mode_timer.reset()
        sleeping = False
        if not env_data:
            emotions.heartbeat()
            time.sleep(0.8)
    elif mode == MODE_UPSIDE:
        sleeping = False
        if system.god_mode: # existing god mode
            display.rotation = 2
            emotions.god_mode()
            continue
        god_mode_timer.measure()
        if god_mode_timer.elapsed > 60:
            god_mode_timer.reset()
            system.switch_god_mode()
        elif god_mode_timer.elapsed > 0:
            display.rotation = 2
            emotions.god_mode(counter=god_mode_timer.elapsed)
