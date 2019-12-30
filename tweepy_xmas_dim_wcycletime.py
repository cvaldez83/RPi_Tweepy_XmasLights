"""
This python code uses the tweepy module to listen to twitter
for a specific hashtag and turns on the pin_LED for .01 seconds
when found
""" 

from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from datetime import datetime
import RPi.GPIO as GPIO

# # # # # SETUP INFORMATION # # # # #

# The following OAuth information must be obtained by
# creating an app in your developer twitter account
# (https://developer.twitter.com/en/apps)
CONSUMER_KEY = 'mySrItyW5ZySIj1cDaysjMqfv'
CONSUMER_SECRET = 'mm2YClGMdHGxQirnZr3nxGbeGzaJeaLM8lisRc9Tc55gsJZq4o'
ACCESS_TOKEN = '1059557863775850496-Q42lfRBG5SdHzuFCs8bUzJDkD5KOnn'
ACCESS_SECRET = 'T8LCZx7PHsPFJMsmjjE3cn3jGJSwknVUYmouxGdiIIHVy'

# Desired twitter hashtag keyword
hashtag = 'xmas'
times = 19

# Raspberry pi LED output pin number
pin_LED = 12

# # # # # END OF SETUP INFORMATION # # # # #

# Sets up the pin_LED as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_LED, GPIO.OUT)
GPIO.setwarnings(False)

#Sets up the OAuth process using the keys and tokens
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)

#Creates the twitter API object
api = API(auth)

freq = 50
red_led = GPIO.PWM(pin_LED, freq)
pause_time = 0.010
steps_duty_cycle = 1
def dim():
   red_led.start(0)
   for i in range(0,100+1,steps_duty_cycle*5):
      red_led.ChangeDutyCycle(i)
      if i >= 99:
         time.sleep(.1)
      time.sleep(pause_time)
   for i in range(100,-1,-steps_duty_cycle):
      red_led.ChangeDutyCycle(i)
      time.sleep(pause_time)

class StdOutListener(StreamListener):
    counter = 0
    start_time = time.time()
    def on_data(self,data):
        # performs the following when hashtag is found
        StdOutListener.counter += 1
        if StdOutListener.counter % times == 0:
           cycle_time = time.time() - StdOutListener.start_time
           dim()
           print('Cycle Time: '+ str(cycle_time) + ' seconds.  Counter: ' + str(StdOutListener.counter))
           StdOutListener.start_time = time.time()
        return True

    def on_error(self,status):
        print('error, status code: ' + status)

#GPIO.cleanup()
#Creates a listener object
listener = StdOutListener()
stream = Stream(auth,listener)

stream.filter(track=[hashtag])
