#!/usr/bin/env python

import tweepy

class SeqTweet(object):
    def __init__(self, c_key, c_secret, a_key, a_secret):
        super(SeqTweet, self).__init__()
        self.c_key = c_key
        self.c_secret = c_secret
        self.a_key = a_key
        self.a_secret = a_secret
        auth = tweepy.OAuthHandler(c_key, c_secret)
        auth.set_access_token(a_key, a_secret)
        self.api = tweepy.API(auth)
    
    def create(self):
        pass
    
    def read(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass

def tweets_to_list(api, tweet_pointer):
    l = []
    done = False
    while not done:
        tweet = api.get_status(id=tweet_pointer)
        if tweet.in_reply_to_status_id_str:
            elem = tweet.text[len(api.me().screen_name) + 2:]
            tweet_pointer = tweet.in_reply_to_status_id_str
        else:
            elem = tweet.text
            done = True
        l.append(elem)
    return l

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

def text_to_list(api, msg, max_payload=140):
    l = []
    chunk = ''
    username = api.me().screen_name
    split_msg = msg.split()
    for word in split_msg:
        if 1 + len(username) + 1 + len(word) > max_payload:
            raise Exception("Word is too big.")
        elif chunk == '':
            chunk = word
        elif 1 + len(username) + 1 + len(chunk) + 1 + len(word) > max_payload:
            l.append(chunk)
            chunk = word
        else:
            chunk = chunk + ' ' + word
    l.append(chunk)
    return l

def main():
    from creds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
    obj = SeqTweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    api = obj.api
    s = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do \
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim \
        ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut \
        aliquip ex ea commodo consequat. Duis aute irure dolor in \
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla \
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
        culpa qui officia deserunt mollit anim id est laborum.'
    tweet_id = list_to_tweets(api, l=text_to_list(api, s))
    print tweet_id
    print "=>"
    print ' '.join(tweets_to_list(api, tweet_id))

if __name__ == '__main__':
    main()
