from repositories.repository import Repository
from models.process import AnalyticProcess, AnalyticProcessIn


class AnalyticRepository(Repository):
    def __init__(self):
        super().__init__(AnalyticProcess)

    def get_by_name(self, name: str) -> AnalyticProcess:
        return self.find_query().filter_by(name=name).first()

    def find_by_id(self, process_id: int) -> AnalyticProcess:
        return self.find_query().filter_by(process_id=process_id).first()

    def create(self, process: AnalyticProcessIn) -> AnalyticProcess:
        new_process = self.model(**process.model_dump())
        return super().create(new_process)

    def update_by_id(self, process_id: int, data: dict) -> AnalyticProcess:
        process = self.find_by_id(process_id)
        if not process:
            raise Exception("Process not found")
        self.session.query(self.model).filter_by(process_id=process_id).update(data)
        self.commit()
        return self.find_by_id(process_id)
