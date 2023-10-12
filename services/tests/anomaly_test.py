from unittest import TestCase
import numpy as np
import pandas as pd
import sys
import os

sys.path.append("../..")
from services.anomaly_services import DetectAnomaly


def create_csv():
    data = np.random.randn(250)
    df = pd.DataFrame(data, columns=["data"])
    df.to_csv("./test.csv")


def delete_csv():
    os.remove("./test.csv")


def create_xlsx():
    data = np.random.randn(250)
    df = pd.DataFrame(data, columns=["data"])
    df.to_excel("./test.xlsx")


def delete_xlsx():
    os.remove("./test.xlsx")


class AnalyticTesting(TestCase):
    def test_create_process_array(self):
        data = np.random.randn(250)
        anomaly_service = DetectAnomaly(data, 20)
        anomaly = anomaly_service.array()
        assert len(anomaly) > 0
        assert type(anomaly) == list

    def test_create_process_csv(self):
        create_csv()
        anomaly_service = DetectAnomaly("./test.csv", 20, main_column="data")
        anomaly = anomaly_service.csv()
        delete_csv()
        assert len(anomaly) > 0
        assert type(anomaly) == list

    def test_create_process_xlsx(self):
        create_xlsx()
        anomaly_service = DetectAnomaly("./test.xlsx", 20, main_column="data")
        anomaly = anomaly_service.xlsx()
        delete_xlsx()
        assert len(anomaly) > 0
        assert type(anomaly) == list
