"""
boot
====================================================

This script runs only once when the device is switched on.

DO NOT CHANGE THIS FILE

Use config.py to configure if needed.

"""

from config import boot

# Name the drive to your heart's content
import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = boot['usb_label']
storage.remount("/", readonly=True)

# Instead of code.py we are using the configured start script
# Configure if needed in config.py
import supervisor
supervisor.set_next_code_file(boot['main_script'])
supervisor.reload()