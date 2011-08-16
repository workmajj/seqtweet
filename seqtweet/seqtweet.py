#!/usr/bin/env python

import tweepy

class SeqTweet(object):
    def __init__(self, c_key, c_secret, a_key, a_secret):
        super(SeqTweet, self).__init__()
        auth = tweepy.OAuthHandler(c_key, c_secret)
        auth.set_access_token(a_key, a_secret)
        self.api = tweepy.API(auth)
    
    @staticmethod
    def _chunk_data(front_pad_size, data, sep=None, max_size=140):
        # For considering @replies on all but the last chunk.
        if front_pad_size >= max_size:
            raise Exception("Front pad size leaves no room for data.")
        chunk_size = max_size - front_pad_size
        l = []
        done = False
        while not done:
            # Last chunk needs no @reply.
            if len(data) <= max_size:
                chunk = data
                done = True
            else:
                # For delimited data, separator is first in subsequent chunks.
                # Ensures concatenating chunks always gives the original data.
                if sep:
                    while data[chunk_size] is not sep:
                        chunk_size -= 1
                        if chunk_size < 1:
                            raise Exception("Chunk is bigger than max size.")
                (chunk, data) = (data[0:chunk_size], data[chunk_size:])
            l.append(chunk)
        return l
    
    @staticmethod
    def _list_to_twitter(api, l, max_size=140):
        l.reverse() # Load backwards to use @replies as pointers.
        tweet_id = None
        for item in l:
            if tweet_id:
                payload = "@%s %s" % (api.me().screen_name, item)
                if len(payload) > max_size:
                    raise Exception("Tweet is too big: %s" % (payload))
                try:
                    tweet = api.update_status(status=payload,
                        in_reply_to_status_id=tweet_id)
                except:
                    raise Exception("Couldn't create Tweet: %s" (payload))
            else:
                payload = "%s" % (item) # No @reply for first item.
                if len(payload) > max_size:
                    raise Exception("Tweet is too big: %s" % (payload))
                try:
                    tweet = api.update_status(status=payload)
                except:
                    raise Exception("Couldn't create Tweet: %s" (payload))
            tweet_id = tweet.id_str
        return tweet_id # Last Tweet is first item in @reply chain.
    
    def _twitter_to_list(api, tweet_id):
        l = []
        done = False
        while not done:
            try:
                tweet = api.get_status(id=tweet_id)
            except:
                raise Exception("Couldn't read Tweet: %s" % (tweet_id))
            if tweet.in_reply_to_status_id_str:
                # Remove @replies from follow-up messages.
                payload = tweet.text[len(api.me().screen_name) + 2:]
                tweet_id = tweet.in_reply_to_status_id_str
            else:
                payload = tweet.text
                done = True
            l.append(payload)
        return l
    
    def create(self, data, sep=None):
        pass
    
    def read(self, tweet_id):
        pass
    
    def update(self, tweet_id, data, sep=None):
        pass
    
    def delete(self, tweet_id):
        pass

def twitter_to_list(api, tweet_id):
    l = []
    done = False
    while not done:
        try:
            tweet = api.get_status(id=tweet_id)
        except:
            raise Exception("Couldn't read Tweet: %s" % (tweet_id))
        if tweet.in_reply_to_status_id_str:
            # Remove the @reply from follow-up messages.
            data = tweet.text[len(api.me().screen_name) + 2:]
            tweet_id = tweet.in_reply_to_status_id_str
        else:
            data = tweet.text
            done = True
        l.append(data)
    return l

def list_to_twitter(api, l, max_size=140):
    # Load backwards to use @replies as pointers.
    l.reverse()
    tweet_id = None
    for item in l:
        if tweet_id:
            data = "@%s %s" % (api.me().screen_name, item)
            if len(data) > max_size:
                raise Exception("Tweet is too big: %s" % (data))
            try:
                tweet = api.update_status(status=data,
                    in_reply_to_status_id=tweet_id)
            except:
                raise Exception("Couldn't create Tweet: %s" (data))
        else:
            data = "%s" % (item)
            if len(data) > max_size:
                raise Exception("Tweet is too big: %s" % (data))
            try:
                tweet = api.update_status(status=data)
            except:
                raise Exception("Couldn't create Tweet: %s" (data))
        tweet_id = tweet.id_str
    return tweet_id

def string_to_list(s, pad_size, max_size=140):
    l = []
    chunk = ''
    for word in s.split():
        # First chunk doesn't need an @reply.
        if chunk == '':
            available_size = max_size
        else:
            available_size = max_size - pad_size
        if len(word) > available_size:
            raise Exception("Word is too big: %s" % (word))
        elif chunk == '':
            chunk = word
        elif len(chunk + ' ' + word) > available_size:
            l.append(chunk)
            chunk = word
        else:
            chunk += ' ' + word
    l.append(chunk)
    return l

def main():
    from creds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
    st = SeqTweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    s = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do \
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim \
        ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut \
        aliquip ex ea commodo consequat. Duis aute irure dolor in \
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla \
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
        culpa qui officia deserunt mollit anim id est laborum.'
    tweet_id = list_to_twitter(st.api, string_to_list(s, 10))
    print tweet_id
    print "=>"
    print ' '.join(twitter_to_list(st.api, tweet_id))

if __name__ == '__main__':
    main()
