# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/state/env_sensor
====================================================

Encapsulates SCD40 functionality

@returns {'CO2': xxx, 'Temperature': xx[c|f], 'T_Scale': [c|f], 'Humidity': xx}

"""
import os, adafruit_scd4x

class EnvSense:

    def __init__(self, i2c):
        self.env_sensor = adafruit_scd4x.SCD4X(i2c)
        # SCD40 config
        self.env_sensor.temperature_offset = os.getenv('temperature_offset')
        self.temp_scale = 'c' if os.getenv('temperature_scale') is 'c' else 'f'
        self.env_sensor.altitude = os.getenv('altitude')
        self.env_sensor.co2_offset = os.getenv('co2_offset')
        # Start SCD40
        self.env_sensor.start_periodic_measurement()

    @property
    def data_ready(self):
        return self.env_sensor.data_ready

    @property
    def co2(self):
        return self.env_sensor.CO2 + self.env_sensor.co2_offset

    @property
    def data(self):
        if self.data_ready:
            temperature = self.env_sensor.temperature
            if self.temp_scale is 'f':
                temperature = (temperature * 9/5) + 32
            data = {}
            data['Temperature'] = round(temperature)
            data['T_Scale'] = self.temp_scale
            data['Humidity'] = round(self.env_sensor.relative_humidity)
            data['CO2'] = self.co2
            return data
        return None
