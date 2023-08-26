from polygon import RESTClient
from datetime import datetime, timedelta
import pandas as pd
import re
import requests
from util.Stocks import Stock
from util.BalanceSheet import BalanceSheet
from util.CashFlow import CashFlow
from util.IncomeStatement import IncomeStatement
from data_management.Data_Scraper import DataScraper
import pandas as pd

def financials_decorator(statement_class):

    def decorator(func):

        def wrapper(self, tickers, start_date):
            data = []

            for ticker in tickers:
                df = pd.DataFrame()
                unit = None
                for t in self.client.vx.list_stock_financials(ticker=ticker, filing_date_gte=start_date):
                    date = t.end_date
                    unit = "USD"
                    financial_data = t.financials
                    statement = func(self, financial_data, tickers,
                                     start_date)  # Pass tickers and start_date as arguments

                    for key, item in statement.items():
                        try:
                            value = item.__dict__["value"]
                            df.loc[key, date] = value / self.VALUE_UNIT
                        except AttributeError:
                            pass

                df.dropna(inplace=True, axis=0)

                data.append(statement_class(unit, df))

            return data

        return wrapper

    return decorator

class Polygon(DataScraper):

    VALUE_UNIT = 1000000

    instance = None  # Singleton architecture
    client = None

    def __new__(cls, api_key):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.client = RESTClient(api_key)
        return cls.instance

    def set_api_key(self, api_key):
        self.API_KEY = api_key

    @staticmethod
    def check_date_format(input_string :str):
        # Define a regular expression pattern for "YYYY-MM-DD" format
        pattern = r'^\d{4}-\d{2}-\d{2}$'

        # Use re.match() to check if the input matches the pattern
        if re.match(pattern, input_string):
            return True
        else:
            return False

    def get_close_price(self, tickers, start: str, end: str) -> dict:

        prices = {}

        if not self.check_date_format(start) or not self.check_date_format(end):
            print("Incorrect date format. Has to be YYYY-MM-DD")
            return prices

        for ticker in tickers:

            response = self.client.get_aggs(ticker=ticker, multiplier=1, timespan="day", from_=start, to=end)

            for day in response:
                dict = day.__dict__
                close_price = dict["close"]
                date_object = datetime.fromtimestamp(dict["timestamp"]/1000)

                formatted_date = date_object.strftime('%Y-%m-%d')

                prices[formatted_date] = close_price

        return prices


    @financials_decorator(statement_class=IncomeStatement)
    def get_income_statements(self, financial_data, tickers, start_date: str):
        return financial_data.income_statement.__dict__

    @financials_decorator(statement_class=BalanceSheet)
    def get_balance_sheets(self, financial_data, tickers, start_date: str):
        return financial_data.balance_sheet

    @financials_decorator(statement_class=CashFlow)
    def get_cashflows(self, financial_data, tickers, start_date: str):
        return financial_data.cash_flow_statement.__dict__


p = Polygon("KbD1LkN5_1Kc9adltrkkTnY3eym6jQN3")
d = p.get_balance_sheets(tickers = ["AAPL"], start_date="2023-01-01")
print(d[0].balance_sheet)


