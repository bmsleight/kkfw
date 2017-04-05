import tweepy, time, json
from credentials import *
import requests

import pprint


def putTwiiterStreamMessageToServer(user_id, screen_name, text, me):
    if screen_name != me:
        try:
            r = requests.put('http://' + SERVER_ADDRESS + '/put/tsm', 
                             data = {
                                 'user_id': user_id, 
                                 'screen_name': screen_name,
                                 'text': text
                                 }, 
                             timeout=1)
            return r.status_code
        except:
            return int(404)
    else:
        return int(400)


def directMessageReceived(user_id, screen_name, text, me):
    print("Direct Message User :", user_id, " Screenname: ", 
          screen_name, "Text: ", text)
    putTwiiterStreamMessageToServer(user_id, screen_name, text, me)
    
def openMessageReceived(user_id, screen_name, text, me):
    print("Open Message User :", user_id, " Screenname: ", 
         screen_name, "Text: ", text)
    putTwiiterStreamMessageToServer(user_id, screen_name, text, me)


class StdOutListener( tweepy.StreamListener ):
    def __init__( self, me ):
        self.tweetCount = 0
        self.me = me
        print("I am ", me)
    def on_connect( self ):
        print("Connection established!!")
    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)
    def on_data( self, status ):
        # print("Entered on_data()")
        d = json.loads(status)
        for key in d.keys():
            if key == 'direct_message':
                directMessageReceived(
                  d['direct_message']['sender_id_str'], 
                  d['direct_message']['sender_screen_name'], 
                  d['direct_message']['text'],
                  self.me)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(d)
            if key == 'text':
                openMessageReceived(
                  d['user']['id_str'], 
                  d['user']['screen_name'], 
                  d['text'].split(' ', 1)[1],
                  self.me)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(d)
        return True
    def on_error( self, status ):
        print(status)

def main():
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        print(api.me().screen_name)
        stream = tweepy.Stream(auth, StdOutListener(me=api.me().screen_name))
        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()
