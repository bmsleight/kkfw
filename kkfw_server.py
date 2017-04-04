import hug
import tweepy, time, json
from credentialsreply import *

def returnAPI():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def tweetDM(user_id, text):
    api = returnAPI()
    api.send_direct_message(user_id=user_id, text=text)

def isAFriend(user_a, user_b):
    api = returnAPI()
    return api.exists_friendship(user_a, user_b)


@hug.cli()
@hug.put('/put/tsm')
def twitterStreamMessage(body):
     print(body['text'])
     tweetDM(body['user_id'], "Thanks ....")
