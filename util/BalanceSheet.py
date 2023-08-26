from pandas import DataFrame

class BalanceSheet:

    def __init__(self, unit: str, balance_sheet: DataFrame):
        self.unit = unit
        self.balance_sheet = balance_sheet
