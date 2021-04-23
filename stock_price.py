import yfinance as yf
import datetime as dt
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

class stock_price:

	def __init__(self, company_name):
		self.company_name = company_name

	def get_stock_ticker(self):
		# url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&callback=YAHOO.Finance.SymbolSuggest.ssCallback".format(self.company_name)
		# res = requests.get(url)
		# stock_ticker = res.json()

		url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(self.company_name)
		res = requests.get(url).json()

		stock_ticker = ""
		
		if res["ResultSet"]["Result"]:
			stock_ticker = res["ResultSet"]["Result"][0]["symbol"]

		self.stock_ticker = stock_ticker

	def search_stock(self):

		self.get_stock_ticker()

		stock_obj = yf.Ticker(self.stock_ticker)

		self.stock = stock_obj

	def get_stock_price(self, period, interval):

		self.search_stock()

		df = self.stock.history(period=period, interval=interval)

		self.stock_df = df

		return(df)

	def graph_candle(self):

		fig = go.Figure(data=[go.Candlestick(
			x=self.stock_df.index,
			open=self.stock_df['Open'], high=self.stock_df['High'],
			low=self.stock_df['Low'], close=self.stock_df['Close'],
			increasing_line_color= 'cyan', decreasing_line_color= 'gray'
		)])

		fig.update_xaxes(
			rangeslider_visible=True,
			rangebreaks=[
				# NOTE: Below values are bound (not single values), ie. hide x to y
				dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
				dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
				# dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
			]
		)

		return(fig)


def main():
	print("Hello, this is just a wrapper for getting stock price")
	print()
	print("input company")
	stock = stock_price(input())
	df = stock.get_stock_price("1mo", "1h")

	fig = stock.graph_candle()
	fig.show()


if __name__ == "__main__":
	main()