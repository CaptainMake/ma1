# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/state/eltm
====================================================

Non blocking sensor measurement and state - environment, light, touch & motion

"""

import os, time, board, touchio
import lib_cp_magicalapes.input.motion_lis3dh as ms
import lib_cp_magicalapes.input.sampler_async as sampler_async
import lib_cp_magicalapes.utils as ma_utils
import ma1.state.env_sensor as env_sensor

class LSTM:
        
    def __init__(self, i2c):
        self.motion = ms.Motion_I2C(i2c)
        self.motion.set_defaults(force='2g', threshold=40, tap=2)

        light_threshold = os.getenv('light_threshold')
        self.Light_sampler = sampler_async.Analog('Light', 10, light_threshold, 1, board.A1)
        self.touch_pin = touchio.TouchIn(board.GP2)
        self.Touch_sampler = sampler_async.FeedIn('Touch', 1, 5, 1)
        self.Motion_sampler = sampler_async.FeedIn('Motion', 3, 10, 9)

        self.cal_interval = os.getenv('env_calibration_interval')
        self.env_sense = env_sensor.EnvSense(i2c)
        self._env_data = None
        self.calibration_timer = ma_utils.Timer()

        # [AQI, light, touch, pickup, tilt left, tilt right, upside]
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
        self.Touch_sampler.put(1 if self.touch_pin.value is True else 0)
        x, y, z = self.motion.acceleration
        self.motion_raw = [x, y, z]
        self.Motion_sampler.put(x, y, z)

        if self.env_sense.data_ready:
            self._env_data = self.env_sense.data

        self.prev_state = self.state.copy()
        
        # x, y, z axis averages
        a_x, a_y, a_z = self.Motion_sampler.avg()
        self.motion_avg = [a_x, a_y, a_z]
        # Is it dark
        self.state[0] = 1 if self.Light_sampler.result() else 0
        # Touched
        self.state[1] = 1 if self.Touch_sampler.result()[0] else 0
        # Picked up
        self.state[2] = 1 if -4 >= a_y >= -9.8 else 0
        # Turned to left
        self.state[3] = 1 if a_x >= 9 else 0
        # Turned towards the right
        self.state[4] = 1 if a_x <= -4 else 0
        # upside down
        self.state[5] = 1 if a_z <= -8 else 0        
        # quick move
        self.state[6] = 1 if self.prev_mca - sum(self.motion_avg) > 4 else 0
        
        # Pollution, anything equals or over CO2 800 sets to 1
        if self.env_data:
            self.state[7] = 1 if self.env_data['CO2'] >= 800 else 0
        else:
            self.state[7] = 0
        
        self.prev_mca = sum(self.motion_avg)

    def calibrate():
        self.calibration_timer.measure()
        if self.calibration_timer.elapsed >= self.cal_interval: # configured in settings
            self.calibration_timer.reset()
            self.env_sense.calibrate()    

    # expose samplers
    @property
    def sampler_light(self):
        return self.Light_sampler

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
    def env_data(self):
        return self._env_data

    @property
    def state_changed(self):
        for i in range(8):
            if self.state[i] != self.prev_state[i]:
                return True
        return False

    def equals(self, a):
        for i in range(8):
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
    def touch(self):
        return self._get_state(1)

    @property
    def picked(self):
        return self._get_state(2)

    @property
    def left(self):
        return self._get_state(3)

    @property
    def right(self):
        return self._get_state(4)
    
    @property
    def upside(self):
        return self._get_state(5)

    @property
    def quick_move(self):
        return self._get_state(6)

    @property
    def polluted(self):
        return self._get_state(7)

