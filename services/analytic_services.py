from models.process import AnalyticProcess, AnalyticProcessIn, AnalyticProcessOut
from repositories.analytic_repository import AnalyticRepository
from utils import security
from services.anomaly_services import DetectAnomaly
from database.cache import get_redis
import requests as rq
import json
import os

cache = get_redis()
repository = AnalyticRepository()
ONE_MONTH = 60 * 60 * 24 * 30


def save_anomaly(anomaly: list, process_id: int):
    cache.set(f"anomaly_{process_id}", json.dumps(anomaly), ex=ONE_MONTH)


def get_anomaly(process_id: int):
    return json.loads(cache.get(f"anomaly_{process_id}"))


def delete_temp_file(file: str):
    os.remove(file)


def create_analytics(process_in: AnalyticProcessIn) -> AnalyticProcessOut:
    process = repository.create(process_in)
    token = security.generate_token(process.process_id)
    return AnalyticProcessOut(token=token, **process.__dict__)


def get_service_by_id(process_id: int) -> AnalyticProcess:
    process = repository.find_by_id(process_id)
    if not process:
        raise Exception("Process not found")
    process = process.__dict__
    del process["_sa_instance_state"]
    return AnalyticProcess(**process)


def set_file(process_id: int, file: str) -> AnalyticProcess:
    process = repository.update_by_id(process_id, {"file": file})
    if not process:
        raise Exception("Process not found")
    process = process.__dict__
    del process["_sa_instance_state"]
    return AnalyticProcess(**process)


def send_to_webhook(process: int) -> AnalyticProcess:
    process = repository.find_by_id(process)
    if not process:
        raise Exception("Process not found")
    if not process.webhook:
        raise Exception("Webhook not found")
    data = get_anomaly(process.process_id)
    rq.post(
        process.webhook,
        json={
            "data": data,
            "process_id": process.process_id,
            "process_name": process.name,
        },
        timeout=5,
    )


def analyze_data(process: AnalyticProcess, data: bytes, type: str):
    if not process:
        raise Exception("Process not found")
    temp_file = f"./temp/{process.file}"
    open(temp_file, "wb").write(data)
    detect_anomaly = DetectAnomaly(
        temp_file,
        window_size=process.window_size,
        threshold=process.threshold,
        main_column=process.data_column,
    )
    types = {
        "csv": detect_anomaly.csv,
        "xlsx": detect_anomaly.xlsx,
    }
    analyze = types.get(type)
    if not analyze:
        raise Exception("File type not supported")
    anomaly = analyze()
    repository.update_by_id(process.process_id, {"status": "done"})
    save_anomaly(anomaly, process.process_id)
    send_to_webhook(process.process_id)
