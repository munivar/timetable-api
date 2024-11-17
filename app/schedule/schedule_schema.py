from app.database import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, Time
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.core.utils import generate_unique_key


class ScheduleTable(Base):
    __tablename__ = "schedule_table"  # schedule table
    key = Column(String, primary_key=True, nullable=False, default=generate_unique_key)
    semester = Column(String, default="")
    classRoom = Column(String, default="")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class TimeTable(Base):
    __tablename__ = "time_table"  # time table
    key = Column(String, primary_key=True, nullable=False, default=generate_unique_key)
    schedule_key = Column(
        String, ForeignKey("schedule_table.key", ondelete="CASCADE"), nullable=False
    )
    day = Column(String, index=True)
    time = Column(Time, index=True)
    subject = Column(String, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
