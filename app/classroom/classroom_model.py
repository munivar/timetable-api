from datetime import datetime
from pydantic import BaseModel


class ClassRoomReq(BaseModel):
    name: str


class ClassRoom(BaseModel):
    key: str
    name: str
    created_at: datetime


class ClassRoomRes(BaseModel):
    message: str
    data: ClassRoom


class ClassRoomListRes(BaseModel):
    message: str
    data: list[ClassRoom]
