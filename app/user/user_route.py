from app.user import user_schema, user_model
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2, utils
from app.core.utils import UserAccess


route = APIRouter(prefix="/user", tags=["user"])


@route.get("/fetch", response_model=user_model.UserRes)
def get_user(db: database, authUser: authUser):
    existingUser = (
        db.query(user_schema.UserTable)
        .filter(user_schema.UserTable.key == authUser.key)
        .first()
    )
    if not existingUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    existingAccess = (
        db.query(user_schema.AccessTable)
        .filter(user_schema.AccessTable.user_key == authUser.key)
        .first()
    )
    return {
        "message": "user details fetched",
        "data": existingUser,
        "access": existingAccess,
    }


@route.delete("/delete", response_model=user_model.UserRes)
def delete_user(db: database, authUser: authUser):
    existingUser = (
        db.query(user_schema.UserTable)
        .filter(user_schema.UserTable.key == authUser.key)
        .first()
    )
    if not existingUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    existingAccess = (
        db.query(user_schema.AccessTable)
        .filter(user_schema.AccessTable.user_key == authUser.key)
        .first()
    )
    db.delete(existingUser)
    db.commit()
    return {
        "message": "user details deleted",
        "data": existingUser,
        "access": existingAccess,
    }


@route.post("/register", response_model=user_model.LoginRes)
def reg_admin(reqBody: user_model.RegReq, db: database):
    existingUser = (
        db.query(user_schema.UserTable)
        .filter(user_schema.UserTable.email == reqBody.email)
        .first()
    )
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user already exist"
        )
    if reqBody.role not in ["superadmin", "staff", "student"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid role"
        )
    reqBody.password = utils.hash_password(reqBody.password)
    newUser = user_schema.UserTable(**reqBody.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    # add data in accessTable
    if reqBody.role == "superadmin":
        newAccess = user_schema.AccessTable(
            user_key=newUser.key,
            department=True,
            staff=True,
            classRoom=True,
            subject=True,
            create_timetable=True,
            view_timetable=True,
        )

    if reqBody.role == "staff":
        newAccess = user_schema.AccessTable(
            user_key=newUser.key,
            department=False,
            staff=True,
            classRoom=False,
            subject=True,
            create_timetable=True,
            view_timetable=True,
        )

    if reqBody.role == "student":
        newAccess = user_schema.AccessTable(
            user_key=newUser.key,
            department=False,
            staff=False,
            classRoom=False,
            subject=False,
            create_timetable=False,
            view_timetable=True,
        )

    db.add(newAccess)
    db.commit()
    db.refresh(newAccess)

    regAccessToken = oauth2.create_access_token(data={"user_key": newUser.key})
    return {
        "message": "user details created",
        "token_type": "Bearer",
        "token": regAccessToken,
        "data": newUser,
        "access": newAccess,
    }


@route.post("/login", response_model=user_model.LoginRes)
def login(reqBody: user_model.LoginReq, db: database):
    existingUser = (
        db.query(user_schema.UserTable)
        .filter(user_schema.UserTable.email == reqBody.email)
        .first()
    )
    if not existingUser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credetials"
        )
    existingAccess = (
        db.query(user_schema.AccessTable)
        .filter(user_schema.AccessTable.user_key == existingUser.key)
        .first()
    )
    if not utils.verify_password(reqBody.password, existingUser.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credetials"
        )
    accessToken = oauth2.create_access_token(data={"user_key": existingUser.key})
    return {
        "message": "user details fetched",
        "token_type": "Bearer",
        "token": accessToken,
        "data": existingUser,
        "access": existingAccess,
    }
