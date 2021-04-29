# Stock Sentiment Analyzer Web App

Create a dashboard that combines the stock ticker price trend with aggregated sentiments from social media regarding the observed stock.

Implemented using yfinance, plotly, tweepy, textblob, and streamlit

# Reproducing this web app
To recreate this web app on your own computer, do the following.

### Create conda environment
Firstly, we will create a conda environment called *stock*
```
conda create -n stock python=3.7.9
```
Secondly, we will login to the *stock* environement
```
conda activate stock
```
### Install prerequisite libraries
Pip install libraries
```
pip install -r requirements.txt
```

###  Launch the app

```
streamlit run app.py
```

