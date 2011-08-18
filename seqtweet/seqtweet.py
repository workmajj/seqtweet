#!/usr/bin/env python

import tweepy

class SeqTweet(object):
    def __init__(self, c_key, c_secret, a_key, a_secret):
        super(SeqTweet, self).__init__()
        auth = tweepy.OAuthHandler(c_key, c_secret)
        auth.set_access_token(a_key, a_secret)
        self.api = tweepy.API(auth)
    
    @staticmethod
    def _chunk_data(front_pad_size, data, sep=' ', max_size=140):
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
                # Assumption is that spaces will be added when joining chunks.
                while data[chunk_size] is not sep:
                    chunk_size -= 1
                    if chunk_size < 1:
                        raise Exception("Chunk is bigger than max size.")
                (chunk, data) = (data[0:chunk_size], data[chunk_size + 1:])
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
                    raise Exception("Couldn't create Tweet: %s" % (payload))
            else:
                payload = "%s" % (item) # No @reply for first item.
                if len(payload) > max_size:
                    raise Exception("Tweet is too big: %s" % (payload))
                try:
                    tweet = api.update_status(status=payload)
                except:
                    raise Exception("Couldn't create Tweet: %s" % (payload))
            tweet_id = tweet.id_str
        return tweet_id # Last Tweet is first item in @reply chain.
    
    @staticmethod
    def _twitter_to_list(api, tweet_id):
        l = []
        done = False
        while not done:
            try:
                tweet = api.get_status(id=tweet_id)
            except:
                raise Exception("Couldn't read Tweet: %s" % (tweet_id))
            if tweet.in_reply_to_status_id_str:
                # Remove @replies from follow-up Tweets.
                payload = tweet.text[len(api.me().screen_name) + 2:]
                tweet_id = tweet.in_reply_to_status_id_str
            else:
                payload = tweet.text
                done = True
            l.append(payload)
        return l
    
    @staticmethod
    def _delete_twitter(api, tweet_id):
        next_tweet = None
        done = False
        while not done:
            try:
                tweet = api.get_status(id=tweet_id)
            except:
                raise Exception("Couldn't read Tweet: %s" % (tweet_id))
            if tweet.in_reply_to_status_id_str:
                next_tweet = tweet.in_reply_to_status_id_str
            else:
                done = True
            try:
                api.destroy_status(id=tweet_id)
            except:
                raise Exception("Couldn't delete Tweet: %s" % (tweet_id))
            tweet_id = next_tweet
        return True
    
    def create(self, data, sep=' ', max_size=140):
        at_reply_size = len(self.api.me().screen_name) + 2
        l = self._chunk_data(at_reply_size, data, sep, max_size)
        tweet_id = self._list_to_twitter(self.api, l, max_size)
        return tweet_id
    
    def read(self, tweet_id, sep=' '):
        l = self._twitter_to_list(self.api, tweet_id)
        data = sep.join(l)
        return data
    
    def update(self, tweet_id, data, sep=' ', max_size=140):
        try:
            self._delete_twitter(self.api, tweet_id)
            new_tweet_id = self.create(data, sep, max_size)
        except:
            raise Exception("Couldn't update Tweet: %s" % (tweet_id))
        return new_tweet_id
    
    def delete(self, tweet_id):
        success = self._delete_twitter(self.api, tweet_id)
        return success

def main():
    # Test out the CRUD functions.
    from creds import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
    obj = SeqTweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    s1 = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do ' \
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut ' \
        'enim ad minim veniam, quis nostrud exercitation ullamco laboris ' \
        'nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in ' \
        'reprehenderit in voluptate velit esse cillum dolore eu fugiat ' \
        'nulla pariatur. Excepteur sint occaecat cupidatat non proident, ' \
        'sunt in culpa qui officia deserunt mollit anim id est laborum.'
    print "s1: %s" % (s1)
    tweet_id = obj.create(s1)
    print "Tweets for s1 start at: %s" % (tweet_id)
    data = obj.read(tweet_id)
    print "s1 read from Twitter: %s" % (data)
    print "Are they equal? %s" % (data == s1)
    s2 = 'foo, bar, baz, qux, quux, corge, grault, garply, waldo, fred, ' \
        'plugh, xyzzy, thud, foo, bar, baz, qux, quux, corge, grault, ' \
        'garply, waldo, fred, plugh, xyzzy, thud'
    print "s2: %s" % (s2)
    tweet_id = obj.update(tweet_id, s2)
    print "Updated with s2 starting at: %s" % (tweet_id)
    data = obj.read(tweet_id)
    print "Are they equal? %s" % (data == s2)
    print "Deleted s2 successfully? %s" % (obj.delete(tweet_id))

if __name__ == '__main__':
    main()
