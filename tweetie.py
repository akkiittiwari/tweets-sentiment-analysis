import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    key_items = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(key_items[0], key_items[1])
    auth.set_access_token(key_items[2], key_items[3])
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    response = api.user_timeline(name, count=100)
    tweet_list = list()
    analyzer = SentimentIntensityAnalyzer()

    for res in response:
        tweet_dict = {'id': res.id,
                      'created': res.created_at.date(),
                      'retweeted': res.retweet_count,
                      'text': res.text,
                      'hashtags': res.entities['hashtags'],
                      'urls': res.entities['urls'],
                      'mentions': res.entities['user_mentions'],
                      'score': analyzer.polarity_scores(res.text)
                      }
        tweet_list.append(tweet_dict)
    final_dict = {
        'user': name,
        'count': len(response),
        'tweets': tweet_list
    }
    return final_dict


def fetch_following(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    response = api.friends_ids(name)
    dict_list = list()
    for res in response:
        followed = api.get_user(res)
        user_dict = {
            'name': followed.name,
            'screen_name': followed.screen_name,
            'followers': followed.followers_count,
            'created': followed.created_at.date(),
            'image': followed.profile_image_url
        }
        dict_list.append(user_dict)
    dict_list = sorted(dict_list, key=lambda k: k['followers'], reverse=True)
    return dict_list

