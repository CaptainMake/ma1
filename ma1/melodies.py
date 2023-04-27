# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/melodies
====================================================

Melody constants

"""

import lib_cp_magicalapes.output.sound as ma_sound

# Happy Melodies
HAPPY_1 = (
    (ma_sound.NOTE_C5, 0.2),
    (ma_sound.NOTE_E5, 0.2),
    (ma_sound.NOTE_G5, 0.2),
)

HAPPY_2 = (
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_B5, 0.15),
    (ma_sound.NOTE_E6, 0.3),
)

HAPPY_3 = (
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_B5, 0.15),
    (ma_sound.NOTE_D6, 0.15),
    (ma_sound.NOTE_G6, 0.3),
)

HAPPY_4 = (
    (ma_sound.NOTE_C6, 0.15),
    (ma_sound.NOTE_E6, 0.15),
    (ma_sound.NOTE_G6, 0.15),
    (ma_sound.NOTE_C7, 0.3),
)

HAPPY_5 = (
    (ma_sound.NOTE_E6, 0.2),
    (ma_sound.NOTE_G6, 0.2),
    (ma_sound.NOTE_B6, 0.2),
)

HAPPY_MELODIES = [HAPPY_1, HAPPY_2, HAPPY_3, HAPPY_4, HAPPY_5]

# Startup Melodies
BREAK_1 = (
    (ma_sound.NOTE_G4, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E6, 0.3),
    (ma_sound.NOTE_D6, 0.15),
    (ma_sound.NOTE_G6, 0.15),
    (ma_sound.NOTE_D7, 0.15),
)

BREAK_2 = (
    (ma_sound.NOTE_E4, 0.15),
    (ma_sound.NOTE_G4, 0.15),
    (ma_sound.NOTE_C5, 0.15),
    (ma_sound.NOTE_G5, 0.3),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_D6, 0.15),
)

BREAK_3 = (
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_C5, 0.15),
    (ma_sound.NOTE_E5, 0.3),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_C5, 0.15),
)

BREAK_4 = (
    (ma_sound.NOTE_C5, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E5, 0.3),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
)

BREAK_5 = (
    (ma_sound.NOTE_G4, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_G5, 0.15),
    (ma_sound.NOTE_E5, 0.15),
    (ma_sound.NOTE_C5, 0.3),
)

BREAK_TIME_MELODIES = [BREAK_1, BREAK_2, BREAK_3, BREAK_4, BREAK_5]


BAD_AIR_QUALITY = (
    (ma_sound.NOTE_D5, 0.2),
    (ma_sound.NOTE_FS4, 0.2),
    (ma_sound.NOTE_C4, 0.2),
    (ma_sound.NOTE_A3, 0.2),
    (ma_sound.NOTE_D3, 0.2),
)

