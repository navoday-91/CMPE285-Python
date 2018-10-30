#format values for 2 decimal points
def format_int(i):
    s = str(round(i,2))
    if len(s.split(".")[1]) < 2:
        s += "0"
    return s

def stock_profit_cal():
    #Take Inputs
    symbol = input("Enter the Ticker Symbol:\n")
    allotment = float(input("Enter Allotment:\n"))
    final_price = float(input("Enter Final Stock Price:\n"))
    sell_comm = float(input("Enter Selling Commission:\n"))
    init_price = float(input("Enter Initial Stock Price:\n"))
    buy_comm = float(input("Enter Buying Commission:\n"))
    cap_gain = float(input("Enter Capital Gain Tax Rate (%):\n"))

    #Calculations
    proceeds = allotment*final_price
    init_total = allotment*init_price
    commission = buy_comm + sell_comm
    cost = init_total + commission + ((proceeds - init_total - commission) * (cap_gain/100))
    net_profit = proceeds - cost
    return_on_inv = round((net_profit/cost)*100, 2)
    break_even = (init_total + buy_comm + sell_comm) / allotment
    cap_gain_amt = proceeds - init_total - commission
    cap_gain_tax = cap_gain_amt * (cap_gain/100)

    #Report Generation
    output_rep = "Proceeds\n$"+format_int(proceeds)+"\n\n"
    output_rep += "Cost\n$"+format_int(cost)+"\n\n"
    output_rep += "Cost details:\nTotal Purchase Price:\n"+format_int(allotment)+" X $"+format_int(init_price)+\
                  " = $"+"{:,}".format(init_total)+"\n"
    output_rep += "Buy Commission = $"+format_int(buy_comm)+"\nSell Commission = $"+format_int(sell_comm)+"\n"
    output_rep += "Tax on Capital Gain = "+format_int(cap_gain)+"% of $"+format_int(cap_gain_amt)
    output_rep += " = $"+format_int(cap_gain_tax) + "\n\n"
    output_rep += "Net Profit\n$" +format_int(net_profit) + "\n\n"
    output_rep += "Return in Investment\n" +format_int(return_on_inv) + "%\n\n"
    output_rep += "To break even, you should have a final share price of\n$" + format_int(break_even)
    output_rep = "\nPROFIT REPORT FOR STOCK - " + symbol + "\n" + output_rep
    return output_rep


if __name__ == '__main__':
    report = stock_profit_cal()
    print(report)