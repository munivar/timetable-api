import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_unique_key():
    return str(uuid.uuid4()).replace("-", "")


class UserAccess:
    superadmin = {
        "department": True,
        "staff": True,
        "class": True,
        "subject": True,
        "timetable": True,
        "canViewTimeTable": True,
    }
    staff = {
        "department": False,
        "staff": True,
        "class": False,
        "subject": True,
        "timetable": True,
        "canViewTimeTable": True,
    }
    student = {
        "department": False,
        "staff": False,
        "class": False,
        "subject": False,
        "timetable": False,
        "canViewTimeTable": True,
    }
