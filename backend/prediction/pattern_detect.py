import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def find_double_tops_and_check_drops(data, min_distance=5, drop_threshold=0.05):
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peaks.append((i, data[i]))
    
    double_tops_and_drops = []
    for i in range(1, len(peaks)):
        if peaks[i][0] - peaks[i-1][0] > min_distance and abs(peaks[i][1] - peaks[i-1][1]) / peaks[i-1][1] < 0.1:
            peak_index = peaks[i][0]
            following_prices = data[peak_index+1:peak_index+1+min_distance]
            if not following_prices.empty:
                min_following_price = following_prices.min()
                drop_occurred = (peaks[i][1] - min_following_price) / peaks[i][1] >= drop_threshold
                double_tops_and_drops.append((peaks[i-1][0], peaks[i][0], drop_occurred))
    
    return double_tops_and_drops

def calculate_significant_drop_opportunity(double_tops_and_drops):
    if not double_tops_and_drops:
        return 0  
    
    significant_drops_count = sum(1 for _, _, drop_occurred in double_tops_and_drops if drop_occurred)
    
    opportunity = significant_drops_count / len(double_tops_and_drops)
    return opportunity

def plot_double_tops(data, double_tops_and_drops):
    plt.figure(figsize=(14,7))

    plt.plot(data.index, data.values, label='Price')

    for first_peak, second_peak, drop_occurred in double_tops_and_drops:
        color = 'red' if drop_occurred else 'blue'
        plt.scatter(data.index[first_peak], data.values[first_peak], color=color)
        plt.scatter(data.index[second_peak], data.values[second_peak], color=color)

    plt.title('Double Tops and Subsequent Drops')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

setTicker = ["AAPL", "MSFT", "GOOGL", "AMZN", "V", "JPM", "JNJ", "WMT", "UNH", "PG", "BTC-USD", "ETH-USD", "TSLA", ]
start_date = '2012-01-01'

df = yf.download(setTicker, start=start_date)




double_tops_results = {}
double_tops_and_drops_results = {}

for ticker in setTicker:

    close_prices = df['Close'][ticker]
    
    double_tops_and_drops = find_double_tops_and_check_drops(close_prices)

    double_tops_and_drops_results[ticker] = double_tops_and_drops
    

for ticker, double_tops_and_drops in double_tops_and_drops_results.items():
    print(f"{ticker} double tops and significant drops: {double_tops_and_drops}")
    opportunity = calculate_significant_drop_opportunity(double_tops_and_drops)
    print(f"Significant drop opportunity for {ticker}: {opportunity:.2%}")