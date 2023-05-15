# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
ma1/quotes
====================================================

Quotes & some jokes

@returns 'a quote or a little joke'

"""
import random

text = [
    "Dream big, work hard, stay focused.",
    "Believe you can and you're halfway there.",
    "Believe in yourself.",
    "Create your own happiness.",
    "Stay positive, stay focused.",
    "Chase your dreams relentlessly.",
    "Spread love and kindness.",
    "In a world where you can be anything, be kind.",
    "Don't wait for opportunity, create it.",
    "Every day is a fresh start.",
    "Be fearless in the pursuit of greatness.",
    "The best way to predict the future is to invent it.",
    "Everything you can imagine is real.",
    "Be the change you wish to see in the world.",
    "You are capable of amazing things.",
    "Find joy in the journey.",
    "Your attitude determines your altitude.",
    "Life is short, make it sweet.",
    "Focus on the good.",
    "Do what you love,love what you do.",
    "Believe in the power of positive thinking.",
    "Be the reason someone smiles today.",
    "Never give up on your dreams.",
    "Stay true to yourself.",
    "Live each day to the fullest.",
    "Your only limit is you.",
    "Make every day count.",
    "The future is yours to create.",
    "Dreams don't work unless you do.",
    "Happiness is a choice.",
    "Live with passion.",
    "Be the change you wish to see.",
    "You are the architect of your life.",
    "Good things come to those who hustle.",
    "Embrace the journey.",
    "You are one in a million.",
    "Do what makes your soul shine.",
    "Keep smiling and let your vibes reflect.",
    "Live, love, laugh.",
    "Dream without fear, love without limits.",
    "Life is tough but so are you.",
    "Success is the best revenge.",
    "Stay humble, hustle hard.",
    "Be yourself; everyone else is taken.",
    "The best is yet to come.",
    "Stay strong, stay positive, stay classy.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Life is a balance of holding on and letting go.",
    "Life is too important to be taken seriously.",
    "Life is about making an impact, not an income.",
    "The harder I work, the luckier I get.",
    "You know, the secret of getting ahead is getting started.",
    "Don't count the days, make the days count.",
    "Don't watch the clock; do what it does. Keep going.",
    "The future starts today, not tomorrow.",
    "You miss 100% of the shots you don't take.",
    "Every moment is a fresh beginning.",
    "Don't wait. The time will never be just right.",
    "Do what you can, with what you have, where you are",
    "Opportunities don't happen. You create them.",
    "The best way to predict the future is to create it.",
    "Don't let yesterday take up too much of today",
    "If opportunity doesn't knock, build a door.",
    "It always seems impossible until it's done",
    "Strive not to be a success, but rather to be of value.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "What do you call a bear with no teeth? A gummy bear!",
    "How does a penguin build its house? Igloos it together!",
    "I used to play piano by ear, but now I use my hands.",
    "I'm friends with 25 letters of the alphabet. Don't know why.",
    "What do you call fake spaghetti? An impasta!",
    "Why don't eggs tell jokes? they might crack up!",
    "Why did the tomato turn red? it saw the salad dressing!",
    "How do you organize a space party? You planet!",
    "I was going to tell you a joke about pizza, but it's cheesy.",
    "What did the ocean say to the shore? Nothing, it just waved!",
    "What's brown and sticky? A stick!",
    "I went to buy some camouflage trousers, but I couldn't find any.",
    "I couldn't figure out how to fasten my seatbelt. Then it clicked!",
    "What did one wall say to the other wall? see you at the corner!",
    "I bought a boat because it was for sail.",
    "I tried to take a picture of some fog. I mist.",
    "When life gives you lemons, make lemonade",
    "Never trust atoms; they make up everything.",
    "You know, blunt pencils are really pointless.",
    "The rotation of Earth really makes my day.",
    "You know, whiteboards are remarkable.",
    "I wanted to be an archaeologist, but my career was in ruins."
]

class Quotes:

    def get(self):
        return random.choice(text)
