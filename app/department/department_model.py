from datetime import datetime
from pydantic import BaseModel


class DepartmentReq(BaseModel):
    name: str
    desc: str


class Department(BaseModel):
    key: str
    name: str
    desc: str
    created_at: datetime


class DepartmentRes(BaseModel):
    message: str
    data: Department


class DepartmentListRes(BaseModel):
    message: str
    data: list[Department]
