import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime
from datetime import timedelta

def main():
    startDate = getStartDate(2015)
    endDate = getEndDate(2016)
    funds = 10000
    company = "mmm"

    ticker = yf.Ticker(company)
    divList = getDividendList(ticker.dividends, startDate, endDate)
    
    for div in divList:
        exDivDate = div[0]
        divAmount = div[1]
        buyDate = getDate(exDivDate, -1, 1)
        buyPrice = getBuyPrice(ticker, buyDate)
        sellDate = getDate(exDivDate, 1, 2)
        sellPrice = getSellPrice(ticker, sellDate)
        # print("exDiv Date: " + str(exDivDate.date()) + "\tDiv Amount: " + str(round(divAmount, 2)) + "\t\tBuy Date: " + str(buyDate.date()) + "\tBuy Price: " + str(round(buyPrice, 2)) + "\t\tSell Date: " + str(sellDate.date()) + "\tSell Price: " + str(round(sellPrice, 2)))


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

if __name__ == '__main__':
    main()