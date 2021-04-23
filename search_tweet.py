import tweepy
from textblob import TextBlob
import sys
import datetime as dt
import pandas as pd


#for this API to work you need to go to developer.twitter.com and create a developer account then generate the below required keys and token.
# consumer_key = '3jmA1BqasLHfItBXj3KnAIGFB'
# consumer_secret = 'imyEeVTctFZuK62QHmL1I0AUAMudg5HKJDfkx0oR7oFbFinbvA'

# access_token = '265857263-pF1DRxgIcxUbxEEFtLwLODPzD3aMl6d4zOKlMnme'
# access_token_secret = 'uUFoOOGeNJfOYD3atlcmPtaxxniXxQzAU4ESJLopA1lbC'

class search_tweet:

	def __init__(self):
		#self.coll = coll
		pass

	def auth(self, consumer_key, consumer_secret, access_token, access_token_secret):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)

		self.api = api

	def get_tweet_sentiments(self, twt_search, twt_cnt):

		public_tweets = self.api.search(twt_search+" #stocks -filter:retweets",count=twt_cnt)

		list_res = []
		for tweet in public_tweets:
			tweet_created = tweet.created_at

			txt_tw = tweet.text

			analysis = TextBlob(txt_tw)

			sentiment = analysis.sentiment.polarity

			if sentiment > 0:
				polarity = "Bullish"
			elif sentiment < 0:
				polarity = "Bearish"
			else:
				polarity = "Neutral"
			
			response = {"access_time":dt.datetime.utcnow(), 'tweet_created':tweet_created, 'Company':twt_search, 'Tweet':txt_tw, 'Sentiment':polarity}
			list_res.append(response)

		self.curr_sentiment = list_res
		
		return(self.curr_sentiment)

	def aggregate_sentiment(self):

		df = pd.DataFrame(self.curr_sentiment)
		agg = df.groupby(["Company","Sentiment"]).agg({"Tweet":"nunique"}).reset_index()
		agg = agg.sort_values(by=["Tweet"], ascending=[False]).reset_index(drop=True)

		self.data_tweet = df

		return(agg["Sentiment"][0])


def main():
	print("Hello, this is just a wrapper for searching tweets")

if __name__ == "__main__":
	main()