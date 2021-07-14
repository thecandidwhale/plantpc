import tweepy
import time
import board
from secrets import *

from adafruit_seesaw.seesaw import Seesaw

# global value for i2c board. Easy access to light sensor when ready.
i2c_bus = board.I2C()

# auth_user_tweepy & post_tweet written by Revekka K. from Twitchess
# twitter account is "@TheMingAralia"
def auth_user_tweepy():
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(token,token_secret)
    api=tweepy.API(auth)
    return api

# tweet function provided by Revekka K.
def post_tweet(data):
    api = auth_user_tweepy()
    api.update_status(data)

# uses Adafruit Seesaw library to check water; returns value from 200(very dry) - 2000(very wet)
def checkWater():
    ss = Seesaw(i2c_bus, addr=0x36)
    touch = ss.moisture_read()
    return touch

# Runs through checkWater func to get back moisture value.
# If value is over 700, then the Marvin is moisturized.
# Anything below 700 but above 500 sends a message that it is running low.
# Anything below 500 and the Marvin needs water.
# Utilizes post_tweet() func to fire off tweet.
def needsWater():
    if checkWater() > 700:
        post_tweet("Hail hydrate.")
    elif checkWater() < 700 and checkWater() > 500:
        post_tweet("I will require water soon.")
    else:
        post_tweet("Water me, please.")

#def needsLight():
    # will need to figure out how to connect light sensor via i2c later
    # might need a new cable

# main loop. runs every 60 minutes.
# bad error message, but I'll figure out debugging later.
try:
    while True:
        water = needsWater()
        if water() > 700:
           print("Hail hydrate.")
        elif water() > 500 and water() < 699:
            print("Going to need hydration soon.")
        else:
            print("I require hydration.")
        time.sleep(3600)

except Exception as e:
    print("Exception")
    print(e)