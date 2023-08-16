import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime
from datetime import timedelta
import math

def main():
    startDate = getStartDate(2010)
    endDate = getEndDate(2022)
    funds = 10000
    company = "psx"
    taxPercent = 0.22

    ticker = yf.Ticker(company)
    divList = getDividendList(ticker.dividends, startDate, endDate)
    
    for div in divList:
        exDivDate = div[0]
        divPrice = round(div[1], 2)
        buyDate = getDate(exDivDate, -1, 1)
        buyPrice = round(getBuyPrice(ticker, buyDate), 2)
        sellDate = getDate(exDivDate, 1, 2)
        sellPrice = round(getSellPrice(ticker, sellDate), 2)
        # print("exDiv Date: " + str(exDivDate.date()) + "\tDiv Price: " + str(divPrice) + "\t\tBuy Date: " + str(buyDate.date()) + "\tBuy Price: " + str(buyPrice) + "\t\tSell Date: " + str(sellDate.date()) + "\tSell Price: " + str(sellPrice))
        funds = captureDividends(funds, taxPercent, buyPrice, sellPrice, divPrice, buyDate, sellDate)


def getDividendList(tickerDividends, startDate, endDate):
    divList = []

    for date, value in tickerDividends.items():
        if (date.tz_localize(None) - startDate).days > 0 and (date.tz_localize(None) - endDate).days < 0:
            divList.append([date.tz_localize(None), value])
    return divList

def getDate(date, direction, numDays):
    buyDate = date + direction * timedelta(days=numDays)
    while not marketIsOpen(buyDate):
        buyDate = buyDate + direction * timedelta(days=1)
    return buyDate

def marketIsOpen(date):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return result.empty == False

def getStartDate(year):
    startingDate = str(year) + "-01-01"
    return datetime.strptime(startingDate, "%Y-%m-%d")

def getEndDate(year):
    endingDate = str(year) + "-12-31"
    return datetime.strptime(endingDate, "%Y-%m-%d")

def getBuyPrice(ticker, date):
    stockHistory = ticker.history(start=date, end=getDate(date,1,1))
    return stockHistory.iloc[0]['Close']

def getSellPrice(ticker, date):
    stockHistory = ticker.history(start=date, end=getDate(date,1,1))
    return stockHistory.iloc[0]['Open']

def captureDividends(funds, taxPercent, buyPrice, sellPrice, divPrice, buyDate, sellDate):
    numShares = math.floor(funds/buyPrice)
    totalBuyAmount = numShares * buyPrice
    funds = funds - totalBuyAmount
    print('\nBuy Date: ' + str(buyDate.date()))
    print('Bought ' + str(numShares) + ' shares for $' + str(buyPrice) + ' per share. Total: $' + str(totalBuyAmount))
    print('Remaining funds: $' + str(funds))

    totalSellAmount = numShares * sellPrice
    funds = funds + totalSellAmount + (divPrice * numShares)
    print('\nSell Date: ' + str(sellDate.date()))
    print('Sold ' + str(numShares) + ' shares for $' + str(sellPrice) + ' per share. Total: $' + str(totalSellAmount))
    print('Received ' + str(numShares) + ' dividends for $' + str(divPrice) + ' per share. Total: $' + str(divPrice * numShares))

    if totalSellAmount > totalBuyAmount:
        tax = taxPercent * ((totalSellAmount - totalBuyAmount) + (divPrice * numShares))
    else:
        tax = taxPercent * (divPrice * numShares)
    funds = funds - tax
    print('\nTotal tax on gains: $' + str(tax))
    print('Funds left after capture: $' + str(funds))
    return funds



if __name__ == '__main__':
    main()