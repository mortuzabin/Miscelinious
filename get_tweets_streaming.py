# -*- coding: cp1252 -*-

import json
import sys
import time
import tweepy

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#set API key and secret
api_key = "Your API key"
api_secret = "Your API secret"

# set access token and secret

access_token = "Your access token"
access_token_secret = "Your access token secret"



auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=False,wait_on_rate_limit_notify=True)


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that receives tweets and print out to the output files

    """
    def __init__(self):
        """
        count the number of tweets being collected in the current file
        """
        self.counter = 0
        #set output file name
        self.output = open('streamer' + '_' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')

    def on_data(self, data):
        """
        when receiving real-time tweets, call the on_status function
        """
        self.on_status(data)

    def on_status(self, status):
        # buffer the tweets
        status = status.rstrip('\r\n ')
        self.output.write(status + '\n')

        self.counter += 1
        if self.counter >= 1000:
            # close current file and open a new file to connect more tweets
            self.output.close()
            self.output = open("streamer" + '_' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
        return

    def on_error(self, status_code):
        # error handling
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        # reconnect after 60 seconds
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return


if __name__ == '__main__':
    l = StdOutListener()

    stream = Stream(auth, l, timeout=60.0)
    while True:
        try:
            ## "Locations" is the bounding box of the spatial region you are collecting tweets from
            # Hint: check these two points (24.55, -124.733) and (49.481267, -60.526262). Where do they locate?
            stream.filter(locations=[-124.733, 24.55, -60.526262, 49.481267])
            #stream.filter(track=['COVID'],locations=[-124.733, 24.55, -60.526262, 49.481267])
            break

        except (Exception, tweepy.TweepError):
            print('\n...Reconnecting in 60 seconds.')
            time.sleep(60)
