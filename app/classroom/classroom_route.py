from app.classroom import classroom_model, classroom_schema
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2


route = APIRouter(prefix="/classroom", tags=["classroom"])


@route.post("/create", response_model=classroom_model.ClassRoomRes)
def create_classroom(reqBody: classroom_model.ClassRoomReq, db: database):
    existingClassRoom = (
        db.query(classroom_schema.ClassRoomTable)
        .filter(classroom_schema.ClassRoomTable.name == reqBody.name)
        .first()
    )
    if existingClassRoom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="classroom already exist"
        )

    newClassRoom = classroom_schema.ClassRoomTable(**reqBody.model_dump())
    db.add(newClassRoom)
    db.commit()
    db.refresh(newClassRoom)
    return {
        "message": "classroom details created",
        "data": newClassRoom,
    }


@route.get("/list", response_model=classroom_model.ClassRoomListRes)
def classroom_list(db: database):
    classRoomList = db.query(classroom_schema.ClassRoomTable).all()
    return {
        "message": "classroom details fetched",
        "data": classRoomList,
    }


@route.get("/fetch/{key}", response_model=classroom_model.ClassRoomRes)
def get_classroom(key: str, db: database):
    existingClassRoom = (
        db.query(classroom_schema.ClassRoomTable)
        .filter(classroom_schema.ClassRoomTable.key == key)
        .first()
    )
    if not existingClassRoom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    return {
        "message": "classroom details fetched",
        "data": existingClassRoom,
    }


@route.delete("/delete/{key}", response_model=classroom_model.ClassRoomRes)
def delete_classroom(key: str, db: database):
    existingClassRoom = (
        db.query(classroom_schema.ClassRoomTable)
        .filter(classroom_schema.ClassRoomTable.key == key)
        .first()
    )
    if not existingClassRoom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    db.delete(existingClassRoom)
    db.commit()
    return {
        "message": "classroom details deleted",
        "data": existingClassRoom,
    }
