from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

def format_int(i):
    s = str(round(i,2))
    if len(s.split(".")[1]) < 2:
        s += "0"
    return s

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/assignment1', methods=['GET'])
def get_assignment1():
    return render_template('assignment1.html')

@app.route('/assignment1', methods=['POST'])
def post_assignment1():
    if request.method == 'POST':
        symbol = request.form['symbol']
        allotment = float(request.form['allotment'])
        final_price = float(request.form['final_price'])
        sell_comm = float(request.form['sell_comm'])
        init_price = float(request.form['init_price'])
        buy_comm = float(request.form['buy_comm'])
        cap_gain = float(request.form['cap_gain'])
        proceeds = allotment*final_price
        init_total = allotment*init_price
        commission = buy_comm + sell_comm
        cost = init_total + commission + ((proceeds - init_total - commission) * (cap_gain/100))
        net_profit = proceeds - cost
        return_on_inv = round((net_profit/cost)*100, 2)
        break_even = (init_total + buy_comm + sell_comm) / allotment
        cap_gain_amt = proceeds - init_total - commission
        cap_gain_tax = cap_gain_amt * (cap_gain / 100)
        profit_rep = [symbol, allotment, proceeds, buy_comm, sell_comm, init_total, net_profit, return_on_inv, cap_gain,
                      break_even, final_price, cap_gain_amt, cap_gain_tax, init_price, cost]
        for i in range(1, len(profit_rep)):
            profit_rep[i] = format_int(float(profit_rep[i]))

        return render_template('assignment1.html', users=profit_rep)


@app.route('/assignment2', methods=['GET'])
def get_assignment2():
    return render_template('assignment2.html')


@app.route('/assignment2', methods=['POST'])
def post_assignment2():
    days = ['','Monday',]
    symbol = request.form['symbol']
    stock = symbol.split(":")
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="
    url += stock[0]
    url += "&interval=5min&apikey=1VS6DHVM3DBWAYOH"
    r = requests.get(url)
    stock_time_series = r.json()
    if "Error Message" in stock_time_series:
        return render_template('assignment2.html', error_data="Error in API Call")
    stock_data = {'name': stock[1], 'symbol': stock[0]}
    today = stock_time_series['Meta Data']['3. Last Refreshed']
    stock_data_today = stock_time_series['Time Series (Daily)'][today]
    stock_data['current'] = stock_data_today['4. close']
    stock_data['change_by_vol'] = round(float(stock_data_today['4. close']) - float(stock_data_today['1. open']),2)
    stock_data['change_by_percent'] = round((stock_data['change_by_vol']/float(stock_data_today['1. open']))*100,2)
    pacific = datetime.now(pytz.timezone('US/Pacific'))
    temp = (pacific.strftime('%a-%b-%d-%H-%M-%S-%Y').split("-"))
    stock_data['time'] = " ".join(temp[:3])
    stock_data['time'] += " " + ":".join(temp[3:6]) + " PDT " + temp[6]
    return render_template('assignment2.html', stock_data = stock_data)




if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
