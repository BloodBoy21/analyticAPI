from repositories.repository import Repository
from models.process import AnalyticProcess, AnalyticProcessIn


class UserRepository(Repository):
    def __init__(self):
        super().__init__(AnalyticProcess)

    def get_by_name(self, name: str) -> AnalyticProcess:
        return self.find_query().filter_by(name=name).first()

    def find_by_id(self, process_id: int) -> AnalyticProcess:
        return self.find_query().filter_by(process_id=process_id).first()

    def create(self, process: AnalyticProcess) -> AnalyticProcess:
        new_process = self.model(**process.dict())
        return super().create(new_process)