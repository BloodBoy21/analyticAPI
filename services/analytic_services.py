from models.process import (
    AnalyticProcess,
    AnalyticProcessIn,
    AnalyticProcessOut,
    AnalyticProcessUpdate,
)
from repositories.analytic_repository import AnalyticRepository
from utils import security
from services.anomaly_services import DetectAnomaly
from database.cache import get_redis
import requests as rq
import json
import os
from utils.bucket import download_file, upload_file
import pandas as pd
import pickle

cache = get_redis()
repository = AnalyticRepository()
ONE_MONTH = 60 * 60 * 24 * 30


def save_anomaly(anomaly: list, process_id: int):
    cache.set(f"anomaly_{process_id}", json.dumps(anomaly), ex=ONE_MONTH)


def get_anomaly(process_id: int):
    return json.loads(cache.get(f"anomaly_{process_id}"))


def save_anomaly_bytes(bytes: bytes, process_id: int):
    cache.set(f"anomaly_{process_id}_bytes", pickle.dumps(bytes), ex=ONE_MONTH)


def get_anomaly_bytes(process_id: int):
    try:
        return pickle.loads(cache.get(f"anomaly_{process_id}_bytes"))
    except:
        return None


def delete_temp_file(file: str):
    os.remove(file)


def create_analytics(process_in: AnalyticProcessIn) -> AnalyticProcessOut:
    process = repository.create(process_in)
    token = security.generate_token(process.process_id)
    return AnalyticProcessOut(token=token, **process.__dict__)


def update_analytics(process_id: int, data: AnalyticProcessUpdate) -> AnalyticProcess:
    process = repository.update_by_id(
        process_id, data.model_dump(exclude_none=True, exclude_unset=True)
    )
    if not process:
        raise Exception("Process not found")
    process = process.__dict__
    del process["_sa_instance_state"]
    return AnalyticProcess(**process)


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


def analyze_data(process: AnalyticProcess, data: bytes, type: str) -> list:
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
    delete_temp_file(temp_file)
    save_anomaly(anomaly, process.process_id)
    send_to_webhook(process.process_id)
    return anomaly


def add_data(process: AnalyticProcess, data: bytes, mime_type: str) -> bytes:
    if not process:
        raise Exception("Process not found")
    original_type = process.file.split(".")[-1]
    temp_file = f"./temp/{process.file}_add"
    open(temp_file, "wb").write(data)
    old_file = download_file(process.file)
    open(process.file, "wb").write(old_file)
    types = {
        "csv": pd.read_csv,
        "xlsx": pd.read_excel,
    }
    read_file = types.get(original_type)
    df1 = read_file(temp_file)
    df2 = read_file(process.file)
    new_df = pd.concat([df1, df2])
    save_types = {
        "csv": new_df.to_csv,
        "xlsx": new_df.to_excel,
    }
    save_file = save_types.get(original_type)
    save_file(process.file)
    new_file_bytes = open(process.file, "rb").read()
    upload_file(new_file_bytes, process.file, mime_type)
    delete_temp_file(temp_file)
    return new_file_bytes
