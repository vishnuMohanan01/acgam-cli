from ..error_lib import *


class CSVCheck:
    """Add checks as private methods and call them in begin() method."""

    def __init__(self, df, is_winners):
        self.df = df
        self.is_winners = is_winners
        self.expected_cols = ["name", "email", "institution name"]

    def __is_winners_check(self):
        if self.is_winners:
            self.expected_cols.append("position")

    def __initial_columns_check(self):
        received_cols = [col.lower() for col in self.df.columns]
        for exp_col in self.expected_cols:
            if exp_col not in received_cols:
                raise InvalidColumns(self.expected_cols, received_cols)

    def __nan_check(self):
        is_nan_in_col = self.df.isnull().any().to_list()
        if True in is_nan_in_col:
            raise GeneralError("The given csv Contains empty cells")

    def __length_check(self):
        col_length = None
        for column in self.df:
            curr_col_len = len(self.df[column].values)
            if col_length is not None:
                if curr_col_len == 0:
                    raise GeneralError(f"Empty columns present.")
                if col_length != curr_col_len:
                    raise GeneralError(f"Columns lengths not same.")
            else:
                curr_col_len = len(self.df[column].values)
                if curr_col_len == 0:
                    raise GeneralError(f"Empty columns present.")

    def begin(self):
        self.__is_winners_check()
        self.__initial_columns_check()
        self.__nan_check()
        self.__length_check()
