
import requests
import pandas as pd
from Data_Management.Data_Scraper import DataScraper
from sec_api import QueryApi, ExtractorApi, XbrlApi
import json
from datetime import datetime

def financial_statement_decorator(func):

    def wrapper(self, url):
        filing = self.finanical_statement_api.xbrl_to_json(htm_url=url)
        return func(self, filing)
    return wrapper

class SecClient(DataScraper):

    COMPANY_TICKERS = None
    MAX_FILINGS = "50"



    def __init__(self, email, api_key):

        self.email = email
        self.api_key = api_key
        self.header = {"User-Agent": self.email}
        tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=self.header).json()
        tickers = pd.DataFrame.from_dict(tickers, orient="index")
        tickers["cik_str"] = tickers["cik_str"].astype(str).str.zfill(
            10)  # pad number with leading 0s to make it a 10-digit number
        self.COMPANY_TICKERS = tickers
        self. query_api = QueryApi(api_key = self.api_key)
        self.finanical_statement_api = XbrlApi(self.api_key)

    def get_10q_urls(self, ticker: str, start_year: str, end_year = str(datetime.now().year) ) -> list: #default end_year set to today's year

        query = {
            "query": {"query_string": {
                "query": f"ticker:{ticker} AND filedAt:[{start_year}-01-01 TO {end_year}-12-31] AND formType:\"10-Q\"",
            }},
            "from": "0",
            "size": self.MAX_FILINGS,
            "sort": [{"filedAt": {"order": "desc"}}]
        }

        response = self.query_api.get_filings(query)

        filing_urls = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))
        return filing_urls

    @financial_statement_decorator
    def get_balance_sheet(self, filingl):

        return filingl["BalanceSheets"]

    @financial_statement_decorator
    def get_is(self, filing):

        return filing["StatementsOfIncome"]

    @financial_statement_decorator
    def get_cashflow_statement(self, filing):

        return filing["StatementsOfCashflows"]







