import pandas as pd
import numpy as np
from typing import Union


class DetectAnomaly:
    def __init__(
        self, data: Union[list, str, bytes], window_size=10, threshold=2, main_column=0
    ):
        self.data = data
        self.window_size = window_size
        self.threshold = threshold
        self.main_column = main_column

    def __detect(self) -> list:
        """
        Detect anomalies in the data using rolling mean and standard deviation
        """
        window_size = self.window_size
        threshold = self.threshold
        data = self.data
        main_column = self.main_column
        data["bottom"] = data[main_column].rolling(window=window_size).mean() - (
            threshold * data[main_column].rolling(window=window_size).std()
        )
        data["top"] = data[main_column].rolling(window=window_size).mean() + (
            threshold * data[main_column].rolling(window=window_size).std()
        )
        data.plot()
        data["anomaly"] = data.apply(
            lambda row: row[main_column]
            if (row[main_column] <= row["bottom"] or row[main_column] >= row["top"])
            else np.nan,
            axis=1,
        )
        data.plot()
        self.data = data
        return data["anomaly"].dropna()

    def csv(self) -> list:
        self.data = pd.read_csv(self.data)
        return self.__detect()

    def array(self) -> list:
        self.data = pd.DataFrame(self.data)
        return self.__detect()

    def xlsx(self) -> list:
        self.data = pd.read_excel(self.data)
        return self.__detect()
