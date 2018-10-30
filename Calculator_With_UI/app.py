from flask import Flask
from flask import render_template
from flask import request

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

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
