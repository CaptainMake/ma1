# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/bitmaps
====================================================

Bitmap config dictionary.

@returns 'specified bitmap config object'

"""

config = {
    "heartbeat": {
        "file": "ma1/assets/heartbeat.bmp",
        "frames": 10,
        "fps": 20,
        "width": 50,
        "height": 50,
        "x": 39,
        "y": 7,
        "invert": True
    },
    "break": [ # list animations will be picked at random
        {
            "file": "ma1/assets/break/break1.bmp",
            "frames": 12,
            "fps": 10,
            "width": 50,
            "height": 50,
            "x": 39,
            "y": 14,
            "invert": True
        },
    ],
    "eyes": {
        "static": {
            "neutral": {
                "file": "ma1/assets/eyes/neutral.pbm",
                "x": 0,
                "y": 0
            },
            "half_closed": {
                "file": "ma1/assets/eyes/half-closed.pbm",
                "x": 0,
                "y": 0
            },
            "happy": {
                "file": "ma1/assets/eyes/half-closed.pbm",
                "x": 0,
                "y": -7
            },
            "good": {
                "file": "ma1/assets/eyes/half-closed.pbm",
                "x": 0,
                "y": 0
            },
            "up": {
                "file": "ma1/assets/eyes/neutral.pbm",
                "x": 0,
                "y": -7
            },
            "sleep": {
                "file": "ma1/assets/eyes/neutral.pbm",
                "x": -10,
                "y": 35
            },
            "polluted": {
                "file": "ma1/assets/eyes/polluted.pbm",
                "x": 0,
                "y": 0
            },
        },
        "anim": {
            "happy": {
                "file": "ma1/assets/eyes/happy.bmp",
                "frames": 10,
                "fps": 80,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "good": {
                "file": "ma1/assets/eyes/good.bmp",
                "frames": 10,
                "fps": 80,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "giggle": {
                "file": "ma1/assets/eyes/giggle.bmp",
                "frames": 5,
                "fps": 40,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "giggle_up": {
                "file": "ma1/assets/eyes/giggle.bmp",
                "frames": 5,
                "fps": 40,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": -7,
                "invert": True
            },
            "up": {
                "file": "ma1/assets/eyes/up.bmp",
                "frames": 8,
                "fps": 160,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "down": {
                "file": "ma1/assets/eyes/down-left.bmp",
                "frames": 19,
                "fps": 40,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "blink": {
                "file": "ma1/assets/eyes/blink.bmp",
                "frames": 12,
                "fps": 70,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "shake": {
                "file": "ma1/assets/eyes/shake.bmp",
                "frames": 9,
                "fps": 80,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
            "afraid": {
                "file": "ma1/assets/eyes/afraid.bmp",
                "frames": 4,
                "fps": 60,
                "width": 128,
                "height": 64,
                "x": 1,
                "y": 0,
                "invert": True
            },
        }
    }
}

class Bitmaps:

    def get(self, *args):
        value = config
        for arg in args:
            if arg in value:
                value = value[arg]
            else:
                return None
        return value
