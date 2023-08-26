from util.Stocks import Stock
from Accessory_code import YahooScraper


def data_retriever_decorator(func):

    def wrapper(self, stock: Stock, years, items):
        years = sorted(years)
        try:
            df = func(self, stock, years, items)
        except KeyError:
            print("Data not available")
            df = None
        return df
    return wrapper

class Processor:

    @data_retriever_decorator
    def get_p_and_l_data(self, stock: Stock, years, items):
        return stock.get_p_and_l().loc[items, years]

    @data_retriever_decorator
    def get_balance_sheet_data(self, stock: Stock, years, items):
        return stock.get_balance_sheet().loc[items, years]

    @data_retriever_decorator
    def get_cashflow_data(self, stock: Stock, years, items):
        return stock.get_cashflow().loc[items, years]




scraper = YahooScraper.yahoo_scraper()

bs = scraper.balance_sheet_generator("NEL.OL")

print(bs)



















