"""
boot
====================================================

This script runs only once when the device is switched on.

DO NOT CHANGE THIS FILE

Use settings.toml to configure if needed.

"""

import os, storage, supervisor
import lib_cp_magicalapes.system as ma_system

# Name the drive to your heart's content
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = os.getenv('name')

# If a file 'remove_for_normal_operation' exists, MA-1 is inde mode
system = ma_system.System()
if system.god_mode:
    # In god mode, USB drive is readonly for MA-1 hence writable for humans
    storage.remount("/", readonly=True)
else:
    # Else mounted USB drive is writable for MA-1, hence readonly for Humans
    # Else no sensor calibration data is persisted, MA-1 wont be able to learn
    storage.remount("/", readonly=False)
    

# Notes regarding the god mode and normal operation mode:
# -----------------------------------------------------------------------------
# Since CircuitPython only allows one source (Code or Human) can write at a time,
# We are leaving the mounted storage as read/write for the CircuitPython code
# This makes it read only for the human but writable for the code

# Why we do this?
# - This allows the code to log sensor values, especially environmental sensor calibration values.
# - This also helps to avoid accidental deletion of files from the mounted USB drive.

# How do I switch to the god mode?
# While connected to the USB, Turn MA-2 upside down, wait for approx 60 seconds, you will see the screen shows 'Writable for human'
# Disconnect/connect and now you can change anything to your hearts content

# How do I switch to normal operation mode:
# Connect MA-1 to the computer
# Find a file 'remove_for_normal_operation' and delete
# Disconnect/connect and now your MA-1 is back to the normal operation
# -----------------------------------------------------------------------------


# Instead of code.py we are using the configured start script
# Configure if needed in settings.toml
supervisor.set_next_code_file(os.getenv('main_script'))
supervisor.reload()