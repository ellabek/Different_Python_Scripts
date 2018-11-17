import bs4 as bs
import requests
import csv
import random
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#a.
def save_sp500_tickers():

    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    result_file =  open("qspark_test/outputinrows.csv", 'w')
    result_file.write("ticker_name" + "\n")
    for item in tickers:
        result_file.write(item + "\n")
    result_file.close()

    tickers.insert(0, 'Date')
    with open("qspark_test/outputincolumns.csv", 'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(tickers)

    return tickers
#b.
def pick_randomaly_100(tickers):

    new_list = random.sample(tickers,100)
    return new_list
#c.
def get_historical_data(s_tickers):

    ts = TimeSeries(key='3HJVFO5GEQ61NOQ5', output_format='pandas')
    for symbol in s_tickers:
        data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize = 'full')
        data.to_csv('qspark_test/hist_data/' + symbol + '.csv')

#d.
def calc_cross_correlation(s_tickers):

    #for ticker in s_tickers:
    #use pandas to create a df and check if '2013-03-22' not in data.index?
    #if not - continue to create a new column and add all the data, else ignore this one

    combined_df = pd.DataFrame()
    for ticker in s_tickers:
        df = pd.read_csv('qspark_test/hist_data/' + ticker + '.csv',index_col=['date'],usecols=['date', '4. close'])

        if '2013-03-22' in df.index:
            #make sure the file has 5 years of data - from 22.03.2013
            df = df.drop(df[df.index < '2013-03-22'].index)
            combined_df[ticker] = df['4. close']

    combined_df.to_csv('qspark_test/all_data.csv')

    #cross correlation matrix
    corr_matrix = combined_df.corr().abs()

    #heat map
    # fig, ax = plt.subplots(figsize=(12, 10))  # Sample figsize in inches
    # sns.heatmap(corr_matrix,xticklabels=corr_matrix.columns.values,yticklabels=corr_matrix.columns.values, ax=ax)
    # plt.show()

    return corr_matrix

#e. + f.
def calc_return_highers_pair(corr_matrix):

    #get highest correlated pair
    desc_corr_pairs = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)).stack().sort_values(ascending=False))
    highest_corr_pair = (desc_corr_pairs.index[0])

    two_stocks = pd.DataFrame()
    for stock in highest_corr_pair:
        df = pd.read_csv('qspark_test/hist_data/' + stock + '.csv', index_col=['date'], usecols=['date', '4. close'])
        df = df.drop(df[df.index < '2013-03-22'].index)
        two_stocks[stock] = df['4. close']

    two_stocks.to_csv('qspark_test/two_stocks.csv')

    #return calc
    daily_return = two_stocks/two_stocks.shift(1)-1
    #plot according to return - a lot of noice
    daily_return[highest_corr_pair[0]].plot()
    daily_return[highest_corr_pair[1]].plot()
    plt.show()

    #calc cumulative return
    daily_cumulative_return = (1+daily_return).cumprod()
    #plot according to cumulative return
    daily_cumulative_return.plot()
    plt.show()
    return



#all_tickers = save_sp500_tickers()
#tickers_sample =pick_randomaly_100(all_tickers)
#get_historical_data(tickers_sample)

#after running function a. to c.
tickers_sample = ['.'.join(x.split('.')[:-1]) for x in os.listdir('qspark_test/hist_data/')
                    if os.path.isfile(os.path.join('qspark_test/hist_data/', x))]
corr_matrix = calc_cross_correlation(tickers_sample)
calc_return_highers_pair(corr_matrix)

