
import requests
import pandas as pd
from data_management.Data_Scraper import DataScraper


class SecEdgar(DataScraper):

    COMPANY_TICKERS = None

    def __init__(self, email):

        self.email = email
        self.header = {"User-Agent": self.email}
        tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=self.header).json()
        tickers = pd.DataFrame.from_dict(tickers, orient="index")
        tickers["cik_str"] = tickers["cik_str"].astype(str).str.zfill(
            10)  # pad number with leading 0s to make it a 10-digit number
        self.COMPANY_TICKERS = tickers

    def get_filing_metadata(self, ticker):

        cik_number = self.COMPANY_TICKERS[self.COMPANY_TICKERS["ticker"] == ticker]["cik_str"][0]

        result = self.send_request(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_number}.json", headers = self.header)

        return result

s = SecEdgar("torkjel@hotmail.com")
print(type(s.get_filing_metadata("AAPL")))






