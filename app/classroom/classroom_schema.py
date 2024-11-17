from app.database import Base
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.core.utils import generate_unique_key


class ClassRoomTable(Base):
    __tablename__ = "classroom_table"  # class room table
    key = Column(String, primary_key=True, nullable=False, default=generate_unique_key)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
