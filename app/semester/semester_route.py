from app.semester import semester_model, semester_schema
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2


route = APIRouter(prefix="/semester", tags=["semester"])


@route.post("/create", response_model=semester_model.SemesterRes)
def create_semester(reqBody: semester_model.SemesterReq, db: database):
    existingSemester = (
        db.query(semester_schema.SemesterTable)
        .filter(semester_schema.SemesterTable.name == reqBody.name)
        .first()
    )
    if existingSemester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="semester already exist"
        )

    newSemester = semester_schema.SemesterTable(**reqBody.model_dump())
    db.add(newSemester)
    db.commit()
    db.refresh(newSemester)
    return {
        "message": "semester details created",
        "data": newSemester,
    }


@route.get("/list", response_model=semester_model.SemesterListRes)
def semester_list(db: database):
    semesterList = db.query(semester_schema.SemesterTable).all()
    return {
        "message": "semester details fetched",
        "data": semesterList,
    }


@route.get("/fetch/{key}", response_model=semester_model.SemesterRes)
def get_semester(key: str, db: database):
    existingSemester = (
        db.query(semester_schema.SemesterTable)
        .filter(semester_schema.SemesterTable.key == key)
        .first()
    )
    if not existingSemester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    return {
        "message": "semester details fetched",
        "data": existingSemester,
    }


@route.delete("/delete/{key}", response_model=semester_model.SemesterRes)
def delete_semester(key: str, db: database):
    existingSemester = (
        db.query(semester_schema.SemesterTable)
        .filter(semester_schema.SemesterTable.key == key)
        .first()
    )
    if not existingSemester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    db.delete(existingSemester)
    db.commit()
    return {
        "message": "semester details deleted",
        "data": existingSemester,
    }
