import pandas as pd

class ProcessingError(Exception):
    pass


class DataProcessor:
    def __init__(self, logger):
        self.logger = logger

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = self._normalize(df)
            df = self._apply_business_rules(df)
            df = self._transform(df)
            return df
        except Exception as e:
            raise ProcessingError(e)

    def _normalize(self, df):
        df["name"] = df["name"].str.strip().str.title()
        return df

    def _apply_business_rules(self, df):
        if (df["amount"] <= 0).any():
            raise ProcessingError("Invalid amount detected (<= 0)")
        return df

    def _transform(self, df):
        df["tax"] = df["amount"] * 0.18
        df["net_amount"] = df["amount"] + df["tax"]

        df = df.rename(columns={
            "id": "record_id",
            "name": "customer_name"
        })

        return df

