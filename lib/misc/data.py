from datetime import datetime
from os.path import commonprefix

import pandas as pd

import config
from lib.cloud_utils.storage import Storage


class StockData:
    def __init__(
        self, ticker: str, start_date: datetime = None, end_date: datetime = None
    ):
        self._storage = Storage.instance()
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def get_from_storage(self) -> pd.DataFrame:
        formatted_start_date = self.start_date.strftime("%Y%m%d%H%M")
        formatted_end_date = self.end_date.strftime("%Y%m%d%H%M")
        prefix = commonprefix([formatted_start_date, formatted_end_date])[
            :8
        ]  # down to the day at most
        data_list = self._storage.from_gcs(
            bucket=config.DATA_BUCKET,
            filepath=config.INPUT_PATH + f"/{self.ticker}_5_{prefix}",
        )

        output = pd.DataFrame()
        for data_day in data_list:
            data_day_lines = [
                (line.strip().split(",")[0], float(line.strip().split(",")[1]))
                for line in data_day.strip().split("\n")[1:]
            ]
            output = output.append(data_day_lines)

        output.columns = ["timestamp", "close"]
        output = output[
            output["timestamp"].ge(formatted_start_date)
            & output["timestamp"].le(formatted_end_date)
        ]
        output.set_index("timestamp", drop=True)
        return output
