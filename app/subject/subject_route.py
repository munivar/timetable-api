from app.subject import subject_model, subject_schema
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2


route = APIRouter(prefix="/subject", tags=["subject"])


@route.post("/create", response_model=subject_model.SubjectRes)
def create_subject(reqBody: subject_model.SubjectReq, db: database):
    existingSubject = (
        db.query(subject_schema.SubjectTable)
        .filter(subject_schema.SubjectTable.name == reqBody.name)
        .first()
    )
    if existingSubject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="subject already exist"
        )

    newSubject = subject_schema.SubjectTable(**reqBody.model_dump())
    db.add(newSubject)
    db.commit()
    db.refresh(newSubject)
    return {
        "message": "subject details created",
        "data": newSubject,
    }


@route.get("/list", response_model=subject_model.SubjectListRes)
def subject_list(db: database):
    subjectList = db.query(subject_schema.SubjectTable).all()
    return {
        "message": "subject details fetched",
        "data": subjectList,
    }


@route.get("/fetch/{key}", response_model=subject_model.SubjectRes)
def get_subject(key: str, db: database):
    existingSubject = (
        db.query(subject_schema.SubjectTable)
        .filter(subject_schema.SubjectTable.key == key)
        .first()
    )
    if not existingSubject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    return {
        "message": "subject details fetched",
        "data": existingSubject,
    }


@route.delete("/delete/{key}", response_model=subject_model.SubjectRes)
def delete_subject(key: str, db: database):
    existingSubject = (
        db.query(subject_schema.SubjectTable)
        .filter(subject_schema.SubjectTable.key == key)
        .first()
    )
    if not existingSubject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    db.delete(existingSubject)
    db.commit()
    return {
        "message": "subject details deleted",
        "data": existingSubject,
    }
