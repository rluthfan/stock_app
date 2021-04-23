import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime

from search_tweet import search_tweet
from stock_price import stock_price

twitter_cred = {
	"consumer_key": '3jmA1BqasLHfItBXj3KnAIGFB',
	"consumer_secret": 'imyEeVTctFZuK62QHmL1I0AUAMudg5HKJDfkx0oR7oFbFinbvA',
	"access_token":'265857263-pF1DRxgIcxUbxEEFtLwLODPzD3aMl6d4zOKlMnme',
	"access_token_secret": 'uUFoOOGeNJfOYD3atlcmPtaxxniXxQzAU4ESJLopA1lbC'
}

# App title
st.sidebar.markdown('''
# Stock Sentiment Analyzer
Showing the stock price data and sentiment based on queries
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2021, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 4, 13))
selectedCompany = st.sidebar.text_input("Company Search", "AAPL")

# Retrieving tickers data
# ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
# tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_list) # Select ticker symbol
# #tickerData = yf.Ticker(tickerSymbol) # Get ticker data

# if selectedCompany:
# 	tickerSymbol = selectedCompany
# else:
# 	selectedCompany = tickerSymbol

if not selectedCompany: selectedCompany = "AAPL"

stock = stock_price(selectedCompany)
stock.get_stock_ticker()

st.sidebar.markdown("Stock ticker = {}".format(stock.stock_ticker))

search = search_tweet()
search.auth(consumer_key=twitter_cred["consumer_key"], 
	consumer_secret=twitter_cred["consumer_secret"], 
	access_token=twitter_cred["access_token"], 
	access_token_secret=twitter_cred["access_token_secret"])

tweet_list_sentiment = search.get_tweet_sentiments(stock.stock_ticker, 15)
agg_sentiment = search.aggregate_sentiment()

response_json = {"Aggregate": {"Company": stock.stock_ticker, "Sentiment": agg_sentiment}, "By Tweet": tweet_list_sentiment}

if not stock.stock_ticker:
	st.markdown('''
	# Stock Not Found
	Try other company
	''')
	st.write('---')
else:
	st.markdown('''
	# {} Sentiment for {} 
	'''.format(response_json["Aggregate"]["Sentiment"], response_json["Aggregate"]["Company"]))
	st.write('---')

tickerData = yf.Ticker(stock.stock_ticker) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

# Bollinger bands
#st.header('**Bollinger Bands**')
st.header('**Stock Price Trend**')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# Twitter data
st.header('**Recent Tweets**')
st.write(search.data_tweet.drop(["access_time"],axis=1).set_index(["tweet_created"]))

# Ticker data
st.header('**Ticker data**')
st.write(tickerDf)

# Company summary
st.header('**Company Summary**')
string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)


####
#st.write('---')
#st.write(tickerData.info)
