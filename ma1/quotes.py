# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/quotes
====================================================

Quotes

@returns 'a quote'

"""
import random

text = ["Dream big, work hard, stay focused.","Believe you can and you're halfway there.","Believe in yourself.", "Create your own happiness.", "Stay positive, stay focused.","Chase your dreams relentlessly.", "Spread love and kindness.","In a world where you can be anything, be kind.","Don't wait for opportunity, create it.","Every day is a fresh start.","Be fearless in the pursuit of greatness.","The best way to predict the future is to invent it.","Everything you can imagine is real.","Be the change you wish to see in the world.","You are capable of amazing things.","Find joy in the journey.", "Your attitude determines your altitude.", "Life is short, make it sweet.","Focus on the good.", "Do what you love, love what you do.", "Believe in the power of positive thinking.","Be the reason someone smiles today.", "Never give up on your dreams.", "Stay true to yourself.","Live each day to the fullest.", "Your only limit is you.", "Make every day count.","The future is yours to create.", "Dreams don't work unless you do.","Happiness is a choice.", "Live with passion.", "Be the change you wish to see.","You are the architect of your life.", "Good things come to those who hustle.","Embrace the journey.", "You are one in a million."]

class Quotes:

    def get(self):
        return random.choice(text)
