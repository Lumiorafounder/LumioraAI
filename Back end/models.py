from sqlalchemy import Column, Integer, String
from database import Base


class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    student_class = Column(String)


class TeacherDB(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)


class AttendanceDB(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    date = Column(String)
    status = Column(String)


class FeesDB(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    amount = Column(Integer)
    month = Column(String)
    status = Column(String)


class SubjectDB(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    teacher_id = Column(Integer)