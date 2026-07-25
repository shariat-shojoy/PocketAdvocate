import pandas as pd


class LawLoader:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load(self):
        df = pd.read_csv(self.csv_path)

        # Replace NaN with empty string
        df = df.fillna("")

        return df