class GeneralError(Exception):
    def __init__(self, message):
        self.message = message
        super.__init__(self.message)

    def __str__(self):
        return self.message


class InvalidColumns(Exception):
    def __init__(self, expected_cols, given_cols):
        self.exp_cols = expected_cols
        self.given_cols = given_cols
        self.message = "Invalid Column Names"
        super().__init__(self.message)

    def __str__(self):
        return f"expected column names where {self.exp_cols}.\n but recieved {self.given_cols}."
