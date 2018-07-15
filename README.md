# Twitter Sentiment Analysis

The goal of this project is to learn how to pull twitter data, using the tweepy wrapper around the twitter API, and how to perform simple sentiment analysis using the vaderSentiment library. The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection.

### Authenticating with the twitter API server
Twitter requires that you register as a user and then also create an "app" for which Twitter will give you authentication credentials. These credentials are needed for making requests to the API server. Start by logging in to twitter app management then click on "create new app". It should show you a dialog box where you would fill in your own details.

For the website, you can link to your LinkedIn account or something or even your github account. Leave the "callback URL" blank.

Once you have created that app, go to that app page. Click on the "Keys and Access Tokens" tabs, which shows 4 key pieces that represent your authentication information:
- Consumer Key (API Key)
- Consumer Secret (API Secret)
- Access Token
- Access Token Secret

Under the Permissions tab, make sure that you have your access as "Read only" for this application. This prevents a bug in your software from doing something horrible to your twitter account!

We never encode secrets in source code, consequently, we need to pass that information into our web server every time we launch. To prevent having to type that every time, we will store those keys and secrets in a CSV file format:
- consumer_key, consumer_secret, access_token, access_token_secret

The server then takes a commandline argument indicating the file name of this data. For example, I pass in my secrets via 
- $ sudo python server.py ~/licenses/twitter.csv

Please keep in mind the limits imposed by the twitter API. For example, you can only do 15 follower list fetches per 15 minute window, but you can do 900 user timeline fetches.


### Mining for tweets
In file tweetie.py (pronounced "tweety pie", get it?) you will create methods to fetch a list of tweets for a given user and a list of users followed by a given user. Function fetch_tweets() returns a dictionary containing:
- user: user's screen name
- count: number of tweets
- tweets: list of tweets

where each tweet is a dictionary containing:
- id: tweet ID
- created: tweet creation date
- retweeted: number of retweets
- text: text of the tweet
- hashtags: list of hashtags mentioned in the tweet
- urls: list of URLs mentioned in the tweet
- mentions: list of screen names mentioned in the tweet
- score: the "compound" polarity score from vader's polarity_scores()

Function fetch_following() returns a dictionary containing:
- name: user's real name
- screen_name: Twitter screen name (e.g., the_antlr_guy)
- followers: number of followers
- created: created date (no time info)
- image: the URL of the profile's image

This information is needed to generate the HTML for the two different kinds of pages.





