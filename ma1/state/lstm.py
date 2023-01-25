# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/state/lstm
====================================================

Non blocking sensor measurement and state - [light, sound, touch, motion...]

"""

import time, board, touchio
import lib_cp_magicalapes.input.motion_lis3dh as ms
import lib_cp_magicalapes.input.sampler_async as sampler_async


class LSTM:
        
    def __init__(self, i2c):
        self.motion = ms.Motion_I2C(i2c)
        self.motion.set_defaults(force='2g', threshold=40, tap=2)
        
        self.Light_sampler = sampler_async.Analog('Light', 10, 1800, 1, board.A1)
        self.Sound_sampler = sampler_async.Analog('Sound', 10, 1.523, 3.3 / 65536, board.A2)
        self.touch_pin = touchio.TouchIn(board.GP2)
        self.Touch_sampler = sampler_async.FeedIn('Touch', 1, 5, 1)
        self.Motion_sampler = sampler_async.FeedIn('Motion', 3, 10, 9)

        # [light, mic, touch, pickup, tilt left, tilt right, upside]
        self.state = [0]*8
        self.prev_state = [0]*8
        
        # previous motion combined (x,y,z) average
        self.prev_mca = 0
        # motion raw (x, y, z)
        self.motion_raw = []
        # motion averages (x, y, z)
        self.motion_avg = []

    def measure(self):
        # Measure
        self.Light_sampler.measure()
        self.Sound_sampler.measure()
        self.Touch_sampler.put(1 if self.touch_pin.value is True else 0)
        x, y, z = self.motion.acceleration
        self.motion_raw = [x, y, z]
        self.Motion_sampler.put(x, y, z)

        self.prev_state = self.state.copy()
        
        # x, y, z axis averages
        a_x, a_y, a_z = self.Motion_sampler.avg()
        self.motion_avg = [a_x, a_y, a_z]
        # Is it dark
        self.state[0] = 1 if self.Light_sampler.result() else 0
        # Do I hear something
        self.state[1] = 1 if self.Sound_sampler.result() else 0
        # Touched
        self.state[2] = 1 if self.Touch_sampler.result()[0] else 0
        # Picked up
        self.state[3] = 1 if -3.5 >= a_y >= -9 else 0
        # Turned 80 degree to left
        self.state[4] = 1 if a_x >= 8 else 0
        # Turned 80 degree to right
        self.state[5] = 1 if a_x <= -8 else 0
        # upside down
        self.state[6] = 1 if a_z <= -8 else 0        
        # quick move
        self.state[7] = 1 if self.prev_mca - sum(self.motion_avg) > 3 else 0
        
        self.prev_mca = sum(self.motion_avg)

    # expose samplers
    @property
    def sampler_light(self):
        return self.Light_sampler

    @property
    def sampler_sound(self):
        return self.Sound_sampler

    @property
    def sampler_touch(self):
        return self.Touch_sampler

    @property
    def sampler_motion(self):
        return self.Motion_sampler

    # expose states

    @property
    def motion_avg_array(self):
        return self.motion_avg

    @property
    def motion_raw_array(self):
        return self.motion_raw

    @property
    def motion_combined_avg(self):
        return sum(self.motion_avg)

    # expose raw state array

    @property
    def state_array(self):
        return self.state

    @property
    def prev_state_array(self):
        return self.prev_state

    @property
    def state_changed(self):
        for i in range(7):
            if self.state[i] != self.prev_state[i]:
                return True
        return False

    def equals(self, a):
        for i in range(7):
            if self.state[i] != self.a[i]:
                return False
        return True

    # return previous and current state array [previous, current]

    def _get_state(self, i):
        return self.prev_state[i], self.state[i]

    @property
    def dark(self):
        return self._get_state(0)

    @property
    def sound(self):
        return self._get_state(1)

    @property
    def touch(self):
        return self._get_state(2)

    @property
    def picked(self):
        return self._get_state(3)

    @property
    def left(self):
        return self._get_state(4)

    @property
    def right(self):
        return self._get_state(5)
    
    @property
    def upside(self):
        return self._get_state(6)

    @property
    def quick_move(self):
        return self._get_state(7)
