
import requests
import pandas as pd
from Data_Management.Data_Scraper import DataScraper
from sec_api import QueryApi
import json
from datetime import datetime


#GET CIK NUMBER METHOD
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


s = SecClient("torkjel@hotmail.com", "ad255c1c23fcdd341df8bb754f07e58c28d4a7f75cc89220c99560d4c6663604")

print(s.get_10q_urls("TSLA", "2020"))





