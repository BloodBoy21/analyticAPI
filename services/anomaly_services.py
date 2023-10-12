import pandas as pd
import numpy as np


class DetectAnomaly:
    def __init__(self, data, window_size=10, threshold=2):
        self.data = pd.DataFrame(data)
        self.data.plot()
        self.window_size = window_size
        self.threshold = threshold

    def detect(self) -> list:
        """
        Detect anomalies in the data using rolling mean and standard deviation
        """
        window_size = self.window_size
        threshold = self.threshold
        data = self.data
        data["bottom"] = data[0].rolling(window=window_size).mean() - (
            threshold * data[0].rolling(window=window_size).std()
        )
        data["top"] = data[0].rolling(window=window_size).mean() + (
            threshold * data[0].rolling(window=window_size).std()
        )
        data.plot()
        data["anomaly"] = data.apply(
            lambda row: row[0]
            if (row[0] <= row["bottom"] or row[0] >= row["top"])
            else np.nan,
            axis=1,
        )
        data.plot()
        self.data = data
        return data["anomaly"].dropna()
