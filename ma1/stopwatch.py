# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/stopwatch
====================================================

A simple stopwatch

"""

from config import life
import time
import lib_cp_magicalapes.utils as utils

class Stopwatch:
    
    def __init__(self, display, tone):
        self.timer = utils.Timer(millis=True)
        self.m = 0
        self.s = 0
        self.display = display
        self.tone = tone        

    def reset(self):
        self.timer.reset()
        self.display.rotation = 0
        self.m = 0
        self.s = 0

    def show(self):
        if self.tone.is_playing:
            self.tone.stop()
        self.timer.measure()
        if 0 <= (self.timer.elapsed % (1000)) <= 100: # update every second
            self.display.rotation = 3
            self.display.fill(0)
            self.display.text(str(self.s), 20, 50, 1, size=3)
            self.display.text(str(self.m)+'m', 20, 90, 1, size=2)
            self.display.show()
            self.s += 1

        if self.s > 60:
            self.tone.play(1000)
            self.s = 0
            self.m += 1
