from unittest import TestCase
import sys

sys.path.append("../..")
import services.analytic_services as analytic_service
from models.process import AnalyticProcessIn, AnalyticProcess, AnalyticProcessOut
from database.db import engine, db


class AnalyticTesting(TestCase):
    def setUp(self):
        db.metadata.create_all(bind=engine, checkfirst=True)

    def test_create_process(self):
        process = AnalyticProcessIn(name="process_1", webhook="http://localhost:8000")
        new_process = analytic_service.create_analytics(process)
        print(new_process)
        assert new_process.status == "pending"
        assert new_process.__class__ == AnalyticProcessOut
        assert type(new_process.token) == str
