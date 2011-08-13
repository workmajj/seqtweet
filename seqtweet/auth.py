#!/usr/bin/env python

import tweepy

def main():
    key = raw_input("Consumer Key: ").strip()
    secret = raw_input("Consumer Secret: ").strip()
    auth = tweepy.OAuthHandler(key, secret)
    print "Authorize: %s" % (auth.get_authorization_url())
    pin = raw_input("PIN: ").strip()
    auth.get_access_token(pin)
    print "Access Key: %s" % (auth.access_token.key)
    print "Access Secret: %s" % (auth.access_token.secret)

if __name__ == '__main__':
    main()
