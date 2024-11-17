from datetime import datetime
from pydantic import BaseModel


class SubjectReq(BaseModel):
    name: str
    teacher: str
    semester: str


class Subject(BaseModel):
    key: str
    name: str
    teacher: str
    semester: str
    created_at: datetime


class SubjectRes(BaseModel):
    message: str
    data: Subject


class SubjectListRes(BaseModel):
    message: str
    data: list[Subject]
