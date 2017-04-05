import hug
import tweepy, time, json
from credentialsreply import *
from messagetemplates import *

import pprint

def returnAPI():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def verbSplit(text):
    if len(text.split(' ', 1)) == 1:
        verb = text.split(' ', 1)[0]
        rest_of_message = ''
    else:
        [verb, rest_of_message] = text.split(' ', 1)
    verb = verb.upper()
    return (verb, rest_of_message)

def databaseJoin(screen_name):
    pass

def joinRequest(api, screen_name):
    '''Process a request to join
       1 - Test if screen_name following kkfw
       2 - Test if kkfw following screen name
       2a - Attempt to follow screen name
       3 - Test already a member (database??)
       4 - DM reply with joining text, url for terms and current game
    '''
    friendships = api.show_friendship(source_screen_name=screen_name,
                                     target_screen_name=SCREEN_NAME)
    if not friendships[0].following:
        api.update_status('@' + screen_name + JOIN_MUST_FOLLOW_ME)
        return False
    elif not friendships[0].followed_by:
        api.create_friendship(screen_name=screen_name)
        friendships = api.show_friendship(
                                     source_screen_name=screen_name,
                                     target_screen_name=SCREEN_NAME)
        if not friendships[0].followed_by:
            # Unable to follow - restricted twitter account
            api.update_status('@' + screen_name + JOIN_MUST_ALLOW_FOLLOW)
            return False
    elif False: # Already in database
            api.update_status('@' + screen_name + JOIN_ALREADY)
            return False
    # All checks passed DM welcome message
    databaseJoin(screen_name)
    api.send_direct_message(screen_name=screen_name, text=JOIN_DM_1)
    api.send_direct_message(screen_name=screen_name, text=JOIN_DM_2)
    api.send_direct_message(screen_name=screen_name, text=JOIN_DM_3)
    return True


def processInComing(user_id, screen_name, text):
    api = returnAPI()
    
    #Split text into Verb and test of message
    (verb, rest_of_message) = verbSplit(text)
    
    #Process verbs
    if verb == 'JOIN':
        joinRequest(api, screen_name)
    

@hug.cli()
@hug.put('/put/tsm')
def twitterStreamMessage(body):
    processInComing(body['user_id'], body['screen_name'], body['text'])
