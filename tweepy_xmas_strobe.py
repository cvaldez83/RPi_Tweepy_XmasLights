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

class StdOutListener(StreamListener):
    def on_data(self,data):
        # performs the following when hashtag is found
        
	print('Hashtag found')
        GPIO.output(pin_LED, True)
        time.sleep(.01)
        GPIO.output(pin_LED,False)       
        return True

    def on_error(self,status):
        print('error, status code: ' + status)

#Creates a listener object
listener = StdOutListener()
stream = Stream(auth,listener)

stream.filter(track=[hashtag])
