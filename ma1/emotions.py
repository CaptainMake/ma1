# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/emotions
====================================================

MA-1's emotions module, override in config if needed

"""

import os, time, random, board, supervisor
import lib_cp_magicalapes.utils as utils
import lib_cp_magicalapes.output.lights as ma_lights
import lib_cp_magicalapes.output.sound as ma_sound
import ma1.quotes as ma1_quotes
import ma1.melodies as ma1_melody

class Emotions:
    
    RESOURCE_PATH = os.getenv('resource_path')

    def __init__(self, display, tone):
        self.timer = utils.Timer(millis=True)
        self.is_sleeping = False
        self.display = display
        self.tone = tone
        self.led_left = ma_lights.LED_PWM(board.GP8, brightness=12000)
        self.led_right = ma_lights.LED_PWM(board.GP14, brightness=12000)
        self.quotes = ma1_quotes.Quotes()


    def _draw_image(self, file, *, color:int = 1, shift_x:int = 0, shift_y:int = 0, over:bool = False):
        if not over:
            self.display.fill(0)
        self.display.draw_image(Emotions.RESOURCE_PATH + file, color, shift_x, shift_y)
        self.display.show()

    @property
    def brightness(self):
        return self.led_left.brightness

    @brightness.setter
    def brightness(self, value:int):
        self.led_left.brightness = value
        self.led_right.brightness = value

    def heartbeat(self, *, repeat:int = 1):
        img = self.RESOURCE_PATH + 'heartbeat.bmp'
        self.display.animate(img, 50, 50, 10, x=39, y=7, invert=True, repeat=repeat)

    # You can either call this method on startup or create something else
    def startup(self):
        for i in range(4):
            self.heartbeat()
            time.sleep(0.8) # closer to human heartbeat
        self.neutral()
        time.sleep(1)
        self.blink()
        self.tone.play(ma_sound.NOTE_G7, 0.01)

    def neutral(self):
        self._draw_image('eyes/neutral.pbm')
        self.led_left.on()
        self.led_right.on()

    def happy(self, anim:bool=False):
        if anim:
            img = self.RESOURCE_PATH + 'eyes/happy.bmp'
            self.display.animate(img, 128, 64, 10, x=1, y=0, invert=True, fps=120)
        else:
            self._draw_image('eyes/half-closed.pbm', shift_y=-7)

    def good(self, anim:bool=False):
        if anim:
            img = self.RESOURCE_PATH + 'eyes/good.bmp'
            self.display.animate(img, 128, 64, 10, x=1, y=0, invert=True, fps=120)
        else:
            self._draw_image('eyes/half-closed.pbm')

    def content(self):
        self._draw_image('eyes/half-closed.pbm', shift_y=-10)

    def blink(self, repeat:int = 1):
        img = self.RESOURCE_PATH + 'eyes/blink.bmp'
        self.display.animate(img, 128, 64, 12, x=1, y=0, invert=True, repeat=repeat, fps=70)

    def shake(self, repeat:int = 1):
        img = self.RESOURCE_PATH + 'eyes/shake.bmp'
        self.display.animate(img, 128, 64, 9, x=1, y=0, invert=True, repeat=repeat, fps=120)

    def afraid(self):
        self.tone.play(ma_sound.NOTE_A3, 0.1)
        img = self.RESOURCE_PATH + 'eyes/afraid.bmp'
        self.display.animate(img, 128, 64, 4, x=1, y=0, invert=True, repeat=30, fps=60)

    def quiet(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self.blink()

    def wonder(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self._draw_image('eyes/neutral.pbm', shift_x=random.randint(-20, 20), shift_y=random.randint(0, 25))

    def eyes_up(self, anim:bool=False):
        if anim:
            img = self.RESOURCE_PATH + 'eyes/up.bmp'
            self.display.animate(img, 128, 64, 8, x=1, y=0, invert=True, fps=120)
        else:
            self._draw_image('eyes/neutral.pbm', shift_y=-7)

    def eyes_down(self):
        img = self.RESOURCE_PATH + 'eyes/down-left.bmp'
        self.display.animate(img, 128, 64, 19, x=1, y=0, invert=True, fps=40)

    def sleep(self):
        self.led_left.off()
        self.led_right.off()
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (5*1000)) <= 100: # update every 5 seconds
            self._draw_image('eyes/neutral.pbm', shift_x=-10, shift_y=35)
            time.sleep(0.5)
            self.display.text('z', 85, 42, 1)
            self.display.show()
            time.sleep(0.5)
            self.display.text('z', 95, 32, 1)
            self.display.show()

    def say_a_quote(self):
        self.display.label(self.quotes.get(), x=14, y=17)

    def need_a_break(self):
        # one time notification only
        self.tone.melody(random.choice(ma1_melody.BREAK_TIME_MELODIES))        
        # Get all break time animations, we are starting with one but users can add their own animations
        break_anim_path = self.RESOURCE_PATH + 'break/'
        animations = self.list_files(break_anim_path, '.bmp')
        img = break_anim_path + random.choice(animations)
        # Show break animation, loop to show for few seconds
        self.display.animate(img, 50, 50, 12, x=39, y=14, invert=True, repeat=6, fps=10)
        self.say_a_quote()
        time.sleep(8)
        self.neutral()
        time.sleep(0.5)
        self.good(anim=True)        

    def hot(self):
        # Notification stays until action is taken
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
                self._draw_image('eyes/polluted.pbm')
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
                    self.shake(3)
            if 0 <= (self.timer.elapsed % (60*1000)) <= 100: # update every 60 seconds
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
        

    def list_files(self, directory, ext):
        files = []
        for file in os.listdir(directory):
            if not file.startswith('.') and file.endswith(ext):
                files.append(file)
        return files
