from pandas import DataFrame


class CashFlow:

    def __init__(self, unit: str, cashflow: DataFrame):
        self.unit = unit
        self.cashflow = cashflow

