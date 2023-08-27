
class Stock:

    def __init__(self, ticker, balance_sheet, p_and_l, cashflow):

            self.ticker = ticker
            self.balance_sheet = balance_sheet
            self.p_and_l = p_and_l
            self.cashflow = cashflow

    def get_balance_sheet(self):
        return self.balance_sheet

    def get_p_and_l(self):
        return self.p_and_l

    def get_cashflow(self):
        return self.cashflow

    def get_ticker(self):
        return self.ticker
