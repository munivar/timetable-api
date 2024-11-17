from app.department import department_model, department_schema
from fastapi import HTTPException, status, APIRouter
from app.database import database
from app.core.oauth2 import authUser
from app.core import oauth2 as oauth2


route = APIRouter(prefix="/department", tags=["department"])


@route.post("/create", response_model=department_model.DepartmentRes)
def create_department(reqBody: department_model.DepartmentReq, db: database):
    existingDepartment = (
        db.query(department_schema.DepartmentTable)
        .filter(department_schema.DepartmentTable.name == reqBody.name)
        .first()
    )
    if existingDepartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="department already exist"
        )

    newDepartment = department_schema.DepartmentTable(**reqBody.model_dump())
    db.add(newDepartment)
    db.commit()
    db.refresh(newDepartment)
    return {
        "message": "department details created",
        "data": newDepartment,
    }


@route.get("/list", response_model=department_model.DepartmentListRes)
def department_list(db: database):
    departmentList = db.query(department_schema.DepartmentTable).all()
    return {
        "message": "department details fetched",
        "data": departmentList,
    }


@route.get("/fetch/{key}", response_model=department_model.DepartmentRes)
def get_department(key: str, db: database):
    existingDepartment = (
        db.query(department_schema.DepartmentTable)
        .filter(department_schema.DepartmentTable.key == key)
        .first()
    )
    if not existingDepartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    return {
        "message": "department details fetched",
        "data": existingDepartment,
    }


@route.delete("/delete/{key}", response_model=department_model.DepartmentRes)
def delete_department(key: str, db: database):
    existingDepartment = (
        db.query(department_schema.DepartmentTable)
        .filter(department_schema.DepartmentTable.key == key)
        .first()
    )
    if not existingDepartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no data result"
        )
    db.delete(existingDepartment)
    db.commit()
    return {
        "message": "department details deleted",
        "data": existingDepartment,
    }
