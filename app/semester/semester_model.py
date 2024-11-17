from datetime import datetime
from pydantic import BaseModel


class SemesterReq(BaseModel):
    name: str


class Semester(BaseModel):
    key: str
    name: str
    created_at: datetime


class SemesterRes(BaseModel):
    message: str
    data: Semester


class SemesterListRes(BaseModel):
    message: str
    data: list[Semester]
