import pandas

from datetime import datetime

WEEK = ['월','화','수','목','금','토','일']
W1   = ['금','토']
W2   = ['일','월']

def discount_one_price(price,date):
    price = float(price)
    if WEEK[date.weekday()] in W1:
        price = price * 1.3
    if WEEK[date.weekday()] in W2:
        price = price * 0.7
    return price