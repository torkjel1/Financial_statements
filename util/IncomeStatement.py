from pandas import DataFrame

class IncomeStatement:

    def __init__(self, unit: str, income_statement: DataFrame):
        self.unit = unit
        self.income_statement = income_statement
