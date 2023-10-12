from unittest import TestCase
import sys

sys.path.append("../..")
import services.analytic_services as analytic_service
from models.process import AnalyticProcessIn, AnalyticProcess, AnalyticProcessOut
from database.db import engine, db
from datetime import datetime


class AnalyticTesting(TestCase):
    def setUp(self):
        db.metadata.create_all(bind=engine, checkfirst=True)

    def test_create_process(self):
        process_name = f"process_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        process = AnalyticProcessIn(name=process_name, webhook="http://localhost:8000")
        new_process = analytic_service.create_analytics(process)
        assert new_process.status == "pending"
        assert new_process.__class__ == AnalyticProcessOut
        assert type(new_process.token) == str
