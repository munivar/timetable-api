from datetime import datetime, time
from pydantic import BaseModel


class ScheduleReq(BaseModel):
    semester: str
    classRoom: str


class ScheduleRes(BaseModel):
    message: str


class Schedule(BaseModel):
    key: str
    semester: str
    classRoom: str
    created_at: datetime


class TimeTable(BaseModel):
    day: str
    time: time
    subject: str


class ScheduleFetch(BaseModel):
    message: str
    data: Schedule
    timetable: list[TimeTable]


class ScheduleListRes(BaseModel):
    message: str
    data: list[Schedule]


# class Subject(BaseModel):
#     key: str
#     name: str
#     teacher: str
#     semester: str
#     created_at: datetime


# class SubjectListRes(BaseModel):
#     message: str
#     data: list[Subject]
