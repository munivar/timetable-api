from app.staff import staff_model, staff_schema
from app.department import department_schema
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2


route = APIRouter(prefix="/staff", tags=["staff"])


@route.post("/create", response_model=staff_model.StaffRes)
def create_staff(reqBody: staff_model.StaffReq, db: database):
    existingStaff = (
        db.query(staff_schema.StaffTable)
        .filter(staff_schema.StaffTable.name == reqBody.name)
        .first()
    )
    if existingStaff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="staff already exist"
        )

    newStaff = staff_schema.StaffTable(**reqBody.model_dump())
    db.add(newStaff)
    db.commit()
    db.refresh(newStaff)

    existingDepartment = (
        db.query(department_schema.DepartmentTable)
        .filter(department_schema.DepartmentTable.name == reqBody.department)
        .first()
    )

    if not existingDepartment:
        newDepart = department_schema.DepartmentTable(name=reqBody.department, desc="")
        db.add(newDepart)
        db.commit()
        db.refresh(newDepart)
    return {
        "message": "staff details created",
        "data": newStaff,
    }


@route.get("/list", response_model=staff_model.StaffListRes)
def staff_list(db: database):
    staffList = db.query(staff_schema.StaffTable).all()
    return {
        "message": "staff details fetched",
        "data": staffList,
    }


@route.get("/fetch/{key}", response_model=staff_model.StaffRes)
def get_staff(key: str, db: database):
    existingStaff = (
        db.query(staff_schema.StaffTable)
        .filter(staff_schema.StaffTable.key == key)
        .first()
    )
    if not existingStaff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    return {
        "message": "staff details fetched",
        "data": existingStaff,
    }


@route.delete("/delete/{key}", response_model=staff_model.StaffRes)
def delete_staff(key: str, db: database):
    existingStaff = (
        db.query(staff_schema.StaffTable)
        .filter(staff_schema.StaffTable.key == key)
        .first()
    )
    if not existingStaff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    db.delete(existingStaff)
    db.commit()
    return {
        "message": "staff details deleted",
        "data": existingStaff,
    }
