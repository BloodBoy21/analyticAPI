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
    return AnalyticProcess(**process.__dict__)
