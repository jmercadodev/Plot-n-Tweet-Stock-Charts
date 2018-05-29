from matplotlib.finance import candlestick_ohlc
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import date
from keys import api
import datetime
import os

def tweet_chart_image(stock):
    today = datetime.date.today()
    photo = open('images/{}.png'.format(stock), 'rb')
    response = api.upload_media(media=photo)
    api.update_status(status='$' + str.upper(stock) + ' Chart ' + str(today), media_ids=[response['media_id']])
    print('Tweet Sent')

def get_quotes(y,m,d):
    start = datetime.datetime(y, m, d)
    end = datetime.datetime.now()
    
    stocks = ['GPRO', 'AMD', 'MU', 'TSLA', 'SNAP', 'GE']
    for stock in stocks:
        df = web.DataReader(stock, "morningstar", start, end)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        df = df.drop("Symbol", axis=1)

        Close = df['Close']
        Close_Ma = Close.rolling(window=90).mean()

        style.use('fivethirtyeight')

        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.1)
        fig.set_size_inches(20.5, 11.5, forward=True)
        plt.title(str.upper(stock))

        close_data = Close.plot(lw=4)
        close_data.yaxis.tick_right()
        close_data.yaxis.set_label_position("right")

        close_ma_data = Close_Ma.plot(lw=4)
        close_ma_data.yaxis.tick_right()
        close_ma_data.yaxis.set_label_position("right")

        plt.ylabel('Price')
        plt.xlabel('Date')
        
        plt.legend(('Close', '90D MA'))        
        plt.savefig('images/{}.png'.format(stock))
        # plt.show()

        plt.close()
        tweet_chart_image(stock)
        os.remove('images/{}.png'.format(stock)) # 
        print('Chart Image Deleted')

get_quotes(2016, 1, 1)
