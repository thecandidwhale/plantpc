import tweepy
import time
import board

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()

def auth_user_tweepy():
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(token,token_secret)
    api=tweepy.API(auth)
    return api

def post_tweet(data):
    api = auth_user_tweepy()
    api.update_status(data)

# uses Seesaw library to check water; returns value from 200(very dry) - 2000(very wet)
def checkWater():
    ss = Seesaw(i2c_bus, addr=0x36)
    touch = ss.moisture_read()
    return touch

#def needsWater():

#def needsLight():