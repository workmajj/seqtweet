SeqTweet
========

Stores arbitrary strings on Twitter by implementing linked lists.

Contact
-------

John J. Workman ([@workmajj](https://twitter.com/workmajj))

Description
-----------

SeqTweet is a library that lets you store arbitrary-length strings on Twitter by implementing [singly linked lists](http://en.wikipedia.org/wiki/Linked_list#Singly.2C_doubly.2C_and_multiply_linked_lists) of Tweets. It builds the lists using Twitter's native properties (e.g., an [@reply](https://support.twitter.com/entries/14023-what-are-replies-and-mentions) is used to point from one list element to the next). Lists built with SeqTweet respond to [CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)-type requests.

The library itself can safely transform strings of any type. (It will chop up an undelimited string into the correct Tweet-sized components, for example.) Because Twitter strips all leading- and trailing-edge whitespace, and replaces multiple spaces with single characters, writing and then reading an undelimited string will not yield the same result. For this reason, any strings you store with SeqTweet should be delimited by single spaces.

Testing & Usage
---------------

1. Select a Twitter account to use for testing, and [set up an API application](https://dev.twitter.com/apps) with read and write permissions. Note the OAuth consumer key and secret.

2. Install SeqTweet from [PyPI](http://pypi.python.org/pypi/SeqTweet). If you have [```pip```](http://guide.python-distribute.org/installation.html) installed, you can type:

        $ sudo pip install seqtweet

3. Run the ```auth.py``` script that comes with SeqTweet, and enter the two OAuth values.

4. Authorize the PIN by following the URL, and the copy the OAuth access key and secret.

5. Now record all four values into the ```creds.py``` script that comes with SeqTweet.

6. At this point you can run SeqTweet from the command line and follow its CRUD tests.

7. To use the SeqTweet library with your own scripts, simply import the object:

        from seqtweet.seqtweet import SeqTweet

8. And then instantiate a SeqTweet object using the appropriate OAuth values, which gives you access to the CRUD functions.

[License](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22_or_.22Modified_BSD_License.22.29)
-------

Copyright (c) 2011, John J. Workman. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* The names of its contributors may not be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
