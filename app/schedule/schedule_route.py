import random
import select
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2
from datetime import datetime, timedelta
from app.subject import subject_model, subject_schema
from app.schedule import schedule_model, schedule_schema


route = APIRouter(prefix="/schedule", tags=["schedule"])


@route.get("/list", response_model=schedule_model.ScheduleListRes)
def subject_list(db: database):
    scheduleList = db.query(schedule_schema.ScheduleTable).all()
    return {
        "message": "schedule details fetched",
        "data": scheduleList,
    }


@route.post("/create", response_model=schedule_model.ScheduleRes)
def create_schedule(reqBody: schedule_model.ScheduleReq, db: database):
    subjectCount = db.query(subject_schema.SubjectTable).count()
    if subjectCount < 5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Add atleast 5 subjects to create a timetable",
        )

    # Query to get the names of subjects
    existingSubjects = db.query(subject_schema.SubjectTable.name).all()
    finalSubject = []
    for subject in existingSubjects:
        finalSubject.append(subject.name)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    startTime = datetime.strptime("07:30 AM", "%I:%M %p")
    timeSlots = [startTime + timedelta(hours=i) for i in range(10)]

    timetableData = []
    for day in days:
        dailySubjects = finalSubject.copy()
        random.shuffle(dailySubjects)
        for slot in timeSlots:
            if dailySubjects:
                timetableData.append(
                    {"day": day, "time": slot.time(), "subject": dailySubjects.pop(0)}
                )
            else:
                break

    # add data in schedule table
    newSchedule = schedule_schema.ScheduleTable(
        semester=reqBody.semester, classRoom=reqBody.classRoom
    )
    db.add(newSchedule)
    db.commit()

    # add data in time table
    for entry in timetableData:
        db_entry = schedule_schema.TimeTable(
            schedule_key=newSchedule.key,
            day=entry["day"],
            time=entry["time"],
            subject=entry["subject"],
        )
        db.add(db_entry)
        db.commit()
    return {"message": "schedule details created"}


@route.get("/fetch/{key}", response_model=schedule_model.ScheduleFetch)
def get_schedule(key: str, db: database):
    existingSchedule = (
        db.query(schedule_schema.ScheduleTable)
        .filter(schedule_schema.ScheduleTable.key == key)
        .first()
    )
    if not existingSchedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )

    # Fetch timetable entries related to the schedule key
    timetableEntries = (
        db.query(schedule_schema.TimeTable)
        .filter(schedule_schema.TimeTable.schedule_key == key)
        .all()
    )

    # Convert timetable entries to the format expected by the response model
    timetableData = [
        {"day": entry.day, "time": entry.time, "subject": entry.subject}
        for entry in timetableEntries
    ]

    # Define the order of days of the week
    day_order = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
    }

    # Sort the timetable data
    timetableData = sorted(
        timetableData, key=lambda x: (day_order[x["day"]], x["time"])
    )

    return {
        "message": "schedule details fetched",
        "data": existingSchedule,
        "timetable": timetableData,
    }
