from unittest import TestCase
import numpy as np
import pandas as pd
import sys

sys.path.append("../..")
from services.anomaly_services import DetectAnomaly


class AnalyticTesting(TestCase):
    def test_create_process(self):
        data = np.random.randn(250)
        anomaly_service = DetectAnomaly(data, 20)
        anomaly = anomaly_service.detect()
        assert len(anomaly) > 0
        assert type(anomaly) == pd.Series
