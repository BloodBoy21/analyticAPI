from database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime

generate_name = lambda x: f"process_{x}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

class AnalyticProcess(db):
    __tablename__ = "analytic_process"
    process_id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True,default= generate_name(process_id))
    description = Column(String,default="")
    status = Column(String,default="pending")
    file = Column(String)
    webhook = Column(String,default="")
    

class AnalyticProcessIn(BaseModel):
  name: str = Field(..., example="process_1")
  description: str = Field(default="")
  webhook: str = Field(...)
  