from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
from util.CashFlow import CashFlow
from util.BalanceSheet import BalanceSheet
from util.IncomeStatement import IncomeStatement
from util.Stocks import Stock



class yahoo_scraper:

    def webpage_loader(self, url):

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        # Wait for the terms and conditions popup to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button[1]")))

        # Click the "Agree" button to accept terms
        agree_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button[1]")
        agree_button.click()

        # Get the page source after the statements have loaded
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def find_dates(self, soup, statement):
        # extract dates
        dates_row = soup.find("div", class_="D(tbr) C($primaryColor)")
        dates = dates_row.find_all("span")

        if statement != "balance_sheet":
            dates = dates[1:]

        dates = [self.year_extractor(date.text) for date in dates][1:]
        return dates

    def extract_financial_data(self, soup, statement, dates):

        df = pd.DataFrame(columns = [c for c in dates])

        fin_rows = soup.find_all("div", {"data-test": "fin-row"})

        for row in fin_rows:
            items = row.find_all("span")

            index = items[0].text
            values = [items[i + 1].text for i in range(len(items) - 1)]


            if statement.lower() == "p&l" or statement.lower() == "cashflow":
                values = values[1:]
            else:
                pass


            if (len(values) == 4):

                df.loc[index] = values

        df = df.dropna(axis=0)

        return df

    def p_and_l_generator(self, ticker: str):

        soup = self.webpage_loader(f"https://finance.yahoo.com/quote/{ticker}/financials?")

        dates = self.find_dates(soup, "p&l")

        df = self.extract_financial_data(soup, "p&l", dates)

        return df

    def cashflow_generator(self, ticker: str ):

        soup = self.webpage_loader(f"https://finance.yahoo.com/quote/{ticker}/cash-flow?")

        dates = self.find_dates(soup, "cashflow")

        df = self.extract_financial_data(soup, "cashflow", dates)

        return df

    def balance_sheet_generator(self, ticker: str):

        soup = self.webpage_loader(f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?")

        dates = self.find_dates(soup, "balance_sheet")

        df = self.extract_financial_data(soup, "balance_sheet", dates)

        return df

    def year_extractor(self, date: str):

        date_pattern = re.compile(r'\d{2}/\d{2}/(\d{4})')

        match = date_pattern.search(date)

        if match:
            return match.group(1)
        else:
            return None

    def scrape_tickers(self, tickers):

        stocks = {}

        for ticker in tickers:
            balance_sheet = self.balance_sheet_generator(ticker)
            p_and_l = self.p_and_l_generator(ticker)
            cashflows = self.cashflow_generator(ticker)

            stocks[ticker] = (Stock(ticker, balance_sheet, p_and_l, cashflows))

        return stocks
