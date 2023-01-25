# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
"""
config
====================================================

Define all config here

"""

# Used in boot.py
boot = {
    # USB label can only be alphanumeric and '-'
    'usb_label': 'Monty',
    'main_script': 'ma1/start.py'
}


life = {
    'name': 'monty',
    # Override to change display
    'resource_path': 'ma1/monty/',
    # State module, override if needed
    'state': 'ma1.state.lstm',
    # Emotions module, override if needed
    'emotions': 'ma1.emotions'
}
