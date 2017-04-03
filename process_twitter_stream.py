import tweepy, time, json
from credentials import *


def directMessageReceived(user_id, screen_name, text):
    print("Direct Message User :", user_id, " Screenname: ", screen_name, "Text: ", text)

def openMessageReceived(user_id, screen_name, text):
    print("Open Message User :", user_id, " Screenname: ", screen_name, "Text: ", text)


class StdOutListener( tweepy.StreamListener ):
    def __init__( self ):
        self.tweetCount = 0
    def on_connect( self ):
        print("Connection established!!")
    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)
    def on_data( self, status ):
        # print("Entered on_data()")
        d = json.loads(status)
        print(d)
        for key in d.keys():
            if key == 'direct_message':
                directMessageReceived(d['direct_message']['sender_id_str'], d['direct_message']['sender_screen_name'], d['direct_message']['text'])
            if key == 'text':
                openMessageReceived(d['user']['id_str'], d['user']['screen_name'], d['text'].split(' ', 1)[1])
        return True
    def on_error( self, status ):
        print(status)

def main():
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        print(api.me().name)
        stream = tweepy.Stream(auth, StdOutListener())
        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()
