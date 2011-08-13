#!/usr/bin/env python

import tweepy

from creds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

def list_to_tweets(api, l, max_payload=140):
    l.reverse()
    last_tweet = None
    for item in l:
        if last_tweet:
            payload = "@%s %s" % (api.me().screen_name, item)
            if len(payload) > max_payload:
                raise Exception("Tweet is too big.")
            tweet = api.update_status(status=payload,
                in_reply_to_status_id=last_tweet)
        else:
            payload = "%s" % (item)
            if len(payload) > max_payload:
                raise Exception("Tweet is too big.")
            tweet = api.update_status(status=payload)
        last_tweet = tweet.id_str
    return last_tweet

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    print list_to_tweets(api, l=range(4))

if __name__ == '__main__':
    main()
