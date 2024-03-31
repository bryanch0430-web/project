import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def find_double_tops_and_check_drops(data, min_distance=5, threshold=0.05):
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peaks.append((i, data[i]))
    
    categorized_double_tops = {
        'double_top_and_down': [],
        'double_top_and_not_down': [],
        'no_double_top': []
    }

    for i in range(1, len(peaks)):
        if peaks[i][0] - peaks[i-1][0] >= min_distance and abs(peaks[i][1] - peaks[i-1][1]) / peaks[i-1][1] < threshold:
            peak_index = peaks[i][0]
            following_prices = data[peak_index+1:peak_index+1+min_distance]
            if not following_prices.empty:
                min_following_price = following_prices.min()
                drop_occurred = (peaks[i][1] - min_following_price) / peaks[i][1] >= threshold
                double_top_type = 'double_top_and_down' if drop_occurred else 'double_top_and_not_down'
                categorized_double_tops[double_top_type].append((peaks[i-1][0], peaks[i][0]))
    
    return categorized_double_tops


def calculate_significant_drop_opportunity(double_tops_and_drops):
    if not double_tops_and_drops:
        return 0  
    
    significant_drops_count = sum(1 for _, _, drop_occurred in double_tops_and_drops if drop_occurred)
    
    opportunity = significant_drops_count / len(double_tops_and_drops)
    
    return opportunity

def plot_double_tops(data, categorized_double_tops):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data.values, label='Price')

    for category, double_tops in categorized_double_tops.items():
        if category == 'double_top_and_down':
            color = 'red'
        elif category == 'double_top_and_not_down':
            color = 'green'
        else:
            continue

        for first_peak, second_peak in double_tops:
            plt.scatter(data.index[first_peak], data.values[first_peak], color=color)
            plt.scatter(data.index[second_peak], data.values[second_peak], color=color)

    plt.title('Double Tops Categorized')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


setTicker = ["AAPL", "MSFT", "GOOGL", "AMZN", "V", "MA", "TSLA", "NVDA", "PYPL", "ADBE", "INTC", "NFLX", "CSCO", "CMCSA", "PEP", "AVGO", "TMUS", "COST", "QCOM", "AMGN", "TXN", "SBUX", "INTU", "AMD", "ISRG", "GILD", "BKNG", "MDLZ", "MU", "ADP", "FISV", "REGN", "ATVI", "BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "BCH-USD", "LINK-USD", "BNB-USD", "ADA-USD", "XLM-USD", "USDT-USD", "EOS-USD", "TRX-USD", "XMR-USD", "XTZ-USD", "NEO-USD", "MIOTA-USD", "DASH-USD", "ETC-USD", "VET-USD", "DOGE-USD", "ZEC-USD", "LSK-USD", "OMG-USD", "QTUM-USD", "ZRX-USD", "BCN-USD", "BTG-USD", "DCR-USD", "ICX-USD", "SC-USD", "STEEM-USD", "REP-USD", "GNT-USD", "WAVES-USD", "MKR-USD", "DGB-USD", "BTM-USD", "ETN-USD", "BCD-USD", "HC-USD", "KCS-USD", "ETP-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", " RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD",]
start_date = '2012-01-01'

df = yf.download(setTicker, start=start_date)



double_tops_results = {}

for ticker in setTicker:
    close_prices = df['Close'][ticker]
    categorized_double_tops = find_double_tops_and_check_drops(close_prices)
    double_tops_results[ticker] = categorized_double_tops
    
    for category, double_tops in categorized_double_tops.items():
        print(f"{ticker} {category}: {len(double_tops)} occurrences")
     
