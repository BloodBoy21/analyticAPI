from database.db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime

generate_name = lambda x: f"process_{x}_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class AnalyticProcess(db):
    __tablename__ = "analytic_process"
    process_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default=generate_name(process_id))
    description = Column(String, default="")
    status = Column(String, default="pending")
    file = Column(String)
    webhook = Column(String, default="")
    data_column = Column(String, default="data")
    window_size = Column(Integer, default=10)
    threshold = Column(Integer, default=2)


class AnalyticProcessIn(BaseModel):
    name: str = Field(...)
    description: str = Field(default="")
    webhook: str = Field(...)
    data_column: str = Field(default="data", alias="dataColumn")
    window_size: int = Field(default=10, alias="windowSize")
    threshold: int = Field(default=2)


class AnalyticProcessOut(BaseModel):
    status: str = Field(...)
    token: str = Field(...)
