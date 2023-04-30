# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/emotions
====================================================

MA-1's emotions module, override in config if needed

"""

import os, time, random, board, supervisor, gc
import lib_cp_magicalapes.utils as utils
import lib_cp_magicalapes.output.lights as ma_lights
import lib_cp_magicalapes.output.sound as ma_sound
import ma1.quotes as ma1_quotes
import ma1.melodies as ma1_melody

class Emotions:

    bitmaps_dictionary = __import__(os.getenv('bitmaps'), globals(), locals(), [], 0)

    def __init__(self, display, tone):
        self.timer = utils.Timer(millis=True)
        self.is_sleeping = False
        self.display = display
        self.tone = tone
        self.led_left = ma_lights.LED_PWM(board.GP8, brightness=12000)
        self.led_right = ma_lights.LED_PWM(board.GP14, brightness=12000)
        self.quotes = ma1_quotes.Quotes()
        self.bitmaps = Emotions.bitmaps_dictionary.Bitmaps()

    def _draw_image(self, file, *, color:int = 1, shift_x:int = 0, shift_y:int = 0, over:bool = False):
        if not over:
            self.display.fill(0)
        self.display.draw_image(file, color, shift_x, shift_y)
        self.display.show()
        gc.collect()

    def _draw_label(self, text, x:int = 0, y:int = 0):
        self.display.label(text, x=x, y=y)
        gc.collect()

    def _draw_static(self, *dict_location, color:int = 1, over:bool = False):
        if not over:
            self.display.fill(0)
        bitmap = self.bitmaps.get(*dict_location)
        if bitmap:
            self.display.draw_image(bitmap['file'], color, bitmap['x'], bitmap['y'])
        self.display.show()
        gc.collect()

    def _play_anim(self, *dict_location, repeat:int = 1):
        bitmap = self.bitmaps.get(*dict_location)
        if not bitmap:
            return
        if isinstance(bitmap, list):
            bitmap = random.choice(bitmap)
        self.display.animate(bitmap['file'], bitmap['width'], bitmap['height'], bitmap['frames'], x=bitmap['x'], y=bitmap['y'], invert=bitmap['invert'], fps=bitmap['fps'], repeat=repeat)
        gc.collect()

    @property
    def brightness(self):
        return self.led_left.brightness

    @brightness.setter
    def brightness(self, value:int):
        self.led_left.brightness = value
        self.led_right.brightness = value

    def heartbeat(self, *, repeat:int = 1):
        self._play_anim('heartbeat', repeat=repeat)

    def startup(self):
        for i in range(4):
            self.heartbeat()
            time.sleep(0.8) # closer to human heartbeat
        self.neutral()
        time.sleep(1)
        self.blink()
        self.tone.play(ma_sound.NOTE_G7, 0.01)

    def neutral(self):
        self._draw_static('eyes', 'static', 'neutral')
        self.led_left.on()
        self.led_right.on()

    def happy(self, anim:bool=False, repeat:int = 1):
        if anim:
            self._play_anim('eyes', 'anim', 'happy', repeat=repeat)
        else:
            self._draw_static('eyes', 'static', 'happy')

    def good(self, anim:bool=False, repeat:int = 1):
        if anim:
            self._play_anim('eyes', 'anim', 'good', repeat=repeat)
        else:
            self._draw_static('eyes', 'static', 'good')

    def giggle(self, anim:bool=False, repeat:int = 1):
        if anim:
            self._play_anim('eyes', 'anim', 'giggle', repeat=repeat)
        else:
            self._draw_static('eyes', 'static', 'good')

    def blink(self, repeat:int = 1):
        self._play_anim('eyes', 'anim', 'blink', repeat=repeat)

    # Randomly either blink or giggle, blink has 3x more probability to be picked (may be)
    def touch(self):
        rand_num = random.randint(1, 4)
        if rand_num <= 3: self.blink()
        else: self.giggle(anim=True, repeat=5)

    def shake(self, repeat:int = 1):
        self._play_anim('eyes', 'anim', 'shake', repeat=repeat)

    def afraid(self, repeat:int = 1):
        self.tone.play(ma_sound.NOTE_A3, 0.1)
        self._play_anim('eyes', 'anim', 'afraid', repeat=repeat)

    def quiet(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self.blink()

    def wonder(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self.blink(2)

    def eyes_up(self, anim:bool=False, repeat:int = 1):
        if anim:
            self._play_anim('eyes', 'anim', 'up', repeat=repeat)
        else:
            self._draw_static('eyes', 'static', 'up')

    def eyes_down(self, repeat:int = 1):
        self._play_anim('eyes', 'anim', 'down', repeat=repeat)

    def sleep(self):
        self.led_left.off()
        self.led_right.off()
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (5*1000)) <= 100: # update every 5 seconds
            self._draw_static('eyes', 'static', 'sleep')
            time.sleep(0.5)
            self.display.text('z', 85, 42, 1)
            self.display.show()
            time.sleep(0.5)
            self.display.text('z', 95, 32, 1)
            self.display.show()

    def say_a_quote_or_joke(self):
        text = self.quotes.get()
        y = 17 if len(text) <= 50 else 11
        self._draw_label(text, x=14, y=y)

    def need_a_break(self):
        self.tone.melody(random.choice(ma1_melody.BREAK_TIME_MELODIES))
        # Get all break time animations, we are starting with one but users can add their own animations
        self._play_anim('break', repeat=6)
        self.say_a_quote_or_joke()
        time.sleep(8)
        self.giggle()
        time.sleep(0.5)
        self.giggle(anim=True, repeat=3)

    def hot(self):
        # Notification stays until the temperature drops
        self.display.fill(0)
        self.display.text('Too hot', 5, 20, 1, size=2)
        self.display.text('Disconnect', 5, 40, 1, size=2)
        self.display.show()
        self.tone.play(ma_sound.NOTE_G7, 2)

    def polluted(self, env_data, *, show_data:bool = False, screen:int = 0):
        if not env_data and not env_data["CO2"]:
            return
        co2 = env_data["CO2"]
        if show_data:
            self.display.fill(0)
            if screen is 0:
                self.display.text('CO2', 7, 20, 1, size=2)
                self.display.text(str(co2), 7, 40, 1, size=2)
                self.display.text('ppm', 7, 55, 1, size=1)
                if co2 < 600:
                    self.display.text('Best', 7, 77, 1, size=2)
                    self.display.text('* * * * *', 7, 97, 1, size=1)
                elif co2 < 800:
                    self.display.text('Good', 7, 77, 1, size=2)
                    self.display.text('* * * *', 7, 97, 1, size=1)
                elif co2 < 1000:
                    self.display.text('Fair', 7, 77, 1, size=2)
                    self.display.text('* * *', 7, 97, 1, size=1)
                elif co2 < 1500:
                    self.display.text('Poor', 7, 77, 1, size=2)
                    self.display.text('* *', 7, 97, 1, size=1)
                else:
                    self.display.text('Bad', 7, 77, 1, size=2)
                    self.display.text('*', 7, 97, 1, size=1)
            else:
                self.display.text('Temp', 7, 20, 1, size=2)
                self.display.text(str(env_data["Temperature"]) + env_data["T_Scale"], 7, 40, 1, size=2)
                self.display.text('Hum', 7, 72, 1, size=2)
                self.display.text(str(env_data["Humidity"]) + '%', 7, 92, 1, size=2)
            self.display.show()
        if co2 >= 1500:
            if not show_data:
                self._draw_static('eyes', 'static', 'polluted')
            self.tone.play(ma_sound.NOTE_DS7, 0.2)
            self.led_left.toggle()
            self.led_right.toggle()
        elif co2 >= 800:
            self.timer.measure()
            if 0 <= (self.timer.elapsed % (5*1000)) <= 100: # update every 5 seconds
                if not show_data:
                    self.blink()
            if 0 <= (self.timer.elapsed % (12*1000)) <= 100: # update every 12 seconds
                if not show_data:
                    self.shake(6)
            if 0 <= (self.timer.elapsed % (90*1000)) <= 100: # update every 90 seconds
                self.tone.play(ma_sound.NOTE_A3, 0.1)
            if 0 <= (self.timer.elapsed % (300*1000)) <= 100: # update every 5 min
                self.tone.melody(ma1_melody.BAD_AIR_QUALITY)

    def god_mode(self, counter:int=0):
        if counter:
            self.display.fill(0)
            self.display.text('God mode ', 16, 15, 1, size=2)
            self.display.text('in ' + str(60-counter)+ 's', 26, 36, 1, size=2)
            self.display.show()
        else:
            self.display.fill(0)
            self.display.text('God mode!', 13, 25, 1, size=2)
            self.display.show()
