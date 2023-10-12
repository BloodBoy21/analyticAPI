from models.process import AnalyticProcess, AnalyticProcessIn, AnalyticProcessOut
from repositories.analytic_repository import AnalyticRepository
from utils import security

repository = AnalyticRepository()


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
