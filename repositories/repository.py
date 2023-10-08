# create parent class for repositories
from typing import Type, Union
from sqlalchemy.orm.decl_api import DeclarativeMeta
from database.db import get_db
from pydantic import BaseModel


class Repository:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, model: Type[DeclarativeMeta]):
        if not hasattr(self, "session"):
            self.session = get_db()
        self.model = model

    def create(
        self, row: Union[BaseModel, DeclarativeMeta]
    ) -> Union[BaseModel, DeclarativeMeta]:
        try:
            self.session.add(row)
            self.commit()
            self.session.refresh(row)
            return row
        except:
            self.session.rollback()
            raise

    def commit(self):
        self.session.commit()

    def find_query(self):
        return self.session.query(self.model)