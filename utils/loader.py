"""Load the JSON statutes used by the legal retrieval index."""

import json
from pathlib import Path

import pandas as pd


class LawLoader:
    """Loads every JSON law file in a directory into one normalized dataframe."""

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def load(self):
        json_files = sorted(self.data_dir.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"No JSON law files found in {self.data_dir.resolve()}")

        records = []
        for json_path in json_files:
            with json_path.open("r", encoding="utf-8") as file:
                rows = json.load(file)

            if not isinstance(rows, list):
                rows = [rows]

            for row_number, row in enumerate(rows, start=1):
                if not isinstance(row, dict):
                    continue
                record = {key: "" if value is None else str(value) for key, value in row.items()}
                record["source_file"] = json_path.name
                record["source_record"] = row_number
                records.append(record)

        if not records:
            raise ValueError("The JSON law files did not contain any object records.")

        return pd.DataFrame(records).fillna("")
