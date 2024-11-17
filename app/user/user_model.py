from datetime import datetime
from pydantic import BaseModel


class LoginReq(BaseModel):
    email: str
    password: str


class RegReq(BaseModel):
    email: str
    name: str
    password: str
    role: str


class Access(BaseModel):
    department: bool
    staff: bool
    classRoom: bool
    subject: bool
    create_timetable: bool
    view_timetable: bool


class User(BaseModel):
    key: str
    name: str
    email: str
    role: str
    created_at: datetime


class UserRes(BaseModel):
    message: str
    data: User
    access: Access


class LoginRes(BaseModel):
    message: str
    token_type: str
    token: str
    data: User
    access: Access
