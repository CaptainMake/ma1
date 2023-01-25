# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/emotions
====================================================

MA-1's emotions module, override in config if needed

"""

from config import life
import time, random, board, supervisor
import lib_cp_magicalapes.utils as utils

class Emotions:
    
    RESOURCE_PATH = life['resource_path']

    def __init__(self, display, tone):
        print('Loading MA-1\'s emotions')
        self.timer = utils.Timer(millis=True)
        self.is_sleeping = False
        self.display = display
        self.tone = tone

    def _draw_image(self, file, color:int = 1, shift_x:int = 0, shift_y:int = 0, over:bool = False):
        if not over:
            self.display.fill(0)
        self.display.draw_image(Emotions.RESOURCE_PATH + file, color, shift_x, shift_y)
        self.display.show()
        
    # You can either call this method on startup or create something else
    def startup(self):
        self.sleep()
        time.sleep(1)
        self.neutral()
        self.tone.play(4800, 0.02)
        self.tone.play(2200, 0.04)

    def neutral(self):
        self._draw_image('eyes/neutral.pbm')

    def happy(self):
        self._draw_image('eyes/half-closed.pbm', 1, 1, 15)

    def good(self):
        self._draw_image('eyes/half-closed.pbm', 1, 1, 15)

    def content(self):
        self._draw_image('eyes/half-closed.pbm')

    def blink(self):
        self._draw_image('eyes/half-closed.pbm', 1)
        self._draw_image('eyes/neutral.pbm')

    def annoyed(self):
        self._draw_image('eyes/annoyed.pbm')

    def dizzy(self):
        self._draw_image('eyes/dizzy.pbm')
        time.sleep(1)

    def quiet(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self.blink()

    def wonder(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (10*1000)) <= 100: # update every 10 seconds
            self._draw_image('eyes/neutral.pbm', 1, random.randint(-20, 20), 35)

    def sleep(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self._draw_image('eyes/neutral.pbm', 1, -10, 44)
            time.sleep(0.5)
            self.display.text('z', 85, 42, 1)
            self.display.show()
            time.sleep(0.5)
            self.display.text('z', 95, 32, 1)
            self.display.show()

    def dream(self):
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (30*1000)) <= 100: # update every 30 seconds
            self.display.fill(0)
            self.display.show()
            time.sleep(0.5)
            self.display.text('z', 12, 57, 1)
            self.display.show()
            time.sleep(0.5)
            self.display.text('z', 20, 51, 1)
            self.display.show()
            img = 'dreams/dream' + str(random.randint(1, 3)) + '.pbm'
            self._draw_image(img, 1, 1, 1, True)
            

    def need_a_break(self):
        # one time notification only
        self._draw_image('break.pbm', 1)
        self.tone.play(1000, 0.04)
        time.sleep(2)

    def hot(self):
        # Notification until action is taken
        self.display.fill(0)
        self.display.text('Too hot', 5, 20, 1, size=2)
        self.display.text('Disconnect', 5, 40, 1, size=2)
        self.display.show()
        self.tone.play(4000, 2)
                    
