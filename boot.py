# SPDX-License-Identifier: MIT
#
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

# If a file 'god_mode.txt' exists, MA-1 is writable / configurable
system = ma_system.System()
if system.god_mode:
    # In god mode, USB drive is readonly for MA-1 hence writable for humans
    storage.remount("/", readonly=True)
else:
    # Else mounted USB drive is writable for MA-1, hence readonly for Humans
    storage.remount("/", readonly=False)

# Notes regarding the god mode and normal operation mode:
# -----------------------------------------------------------------------------
# Since CircuitPython only allows one source (Code or Human) to write at a time,
# We are leaving the mounted storage as read/write for the CircuitPython code
# This makes it read only for the humans but writable for the code

# How do I switch to the god mode?
# While connected to the USB, Turn MA-1 upside down, wait for approx 60 seconds, you will see the screen shows 'God mode!'
# Disconnect/connect and now MA-1 is in God mode and you can change anything to your hearts content

# How do I switch to normal operation mode:
# Connect MA-1 to the computer
# Find a file 'god_mode.txt' and delete
# Disconnect/connect and now your MA-1 is back to the normal operation
# -----------------------------------------------------------------------------


# Instead of code.py we are using the configured start script
# Configure if needed in settings.toml
supervisor.set_next_code_file(os.getenv('main_script'))
supervisor.reload()
