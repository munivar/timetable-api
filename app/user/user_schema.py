from app.database import Base
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.core.utils import generate_unique_key


class UserTable(Base):
    __tablename__ = "user_table"  # user table
    key = Column(String, primary_key=True, nullable=False, default=generate_unique_key)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, default="")
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # superadmin, staff, student
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class AccessTable(Base):
    __tablename__ = "access_table"  # access table
    key = Column(String, primary_key=True, nullable=False, default=generate_unique_key)
    user_key = Column(
        String, ForeignKey("user_table.key", ondelete="CASCADE"), nullable=False
    )
    department = Column(Boolean, nullable=False, default=False)
    staff = Column(Boolean, nullable=False, default=False)
    classRoom = Column(Boolean, nullable=False, default=False)
    subject = Column(Boolean, nullable=False, default=False)
    create_timetable = Column(Boolean, nullable=False, default=False)
    view_timetable = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
