from sqlalchemy import Column, Integer, String
from database import Base


# ---------------- STUDENT TABLE ----------------

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    student_class = Column(String)


# ---------------- TEACHER TABLE ----------------

class TeacherDB(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)


# ---------------- ATTENDANCE TABLE ----------------

class AttendanceDB(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    date = Column(String)
    status = Column(String)