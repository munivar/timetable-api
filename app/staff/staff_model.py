from datetime import datetime
from pydantic import BaseModel


class StaffReq(BaseModel):
    name: str
    desc: str
    department: str
    phone_no: str
    email: str


class Staff(BaseModel):
    key: str
    name: str
    desc: str
    department: str
    phone_no: str
    email: str
    created_at: datetime


class StaffRes(BaseModel):
    message: str
    data: Staff


class StaffListRes(BaseModel):
    message: str
    data: list[Staff]
