from sqlalchemy import Column, Integer, String, Float
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


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)


class MarksDB(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    subject = Column(String)
    marks = Column(Integer)


class ClassDB(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    section = Column(String)
    teacher_id = Column(Integer)


class HomeworkDB(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    subject = Column(String)
    title = Column(String)
    due_date = Column(String)

class ExamDB(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String)
    class_name = Column(String)
    exam_date = Column(String)
    total_marks = Column(Integer)

class TimetableDB(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    day = Column(String)
    subject = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    teacher_id = Column(Integer)

class LeaveDB(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    leave_type = Column(String)
    from_date = Column(String)
    to_date = Column(String)
    reason = Column(String)
    status = Column(String, default="Pending")

class SalaryDB(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_id = Column(String)
    designation = Column(String)
    month = Column(String)
    basic_salary = Column(Float)
    bonus = Column(Float)
    deduction = Column(Float)
    net_salary = Column(Float)
    payment_status = Column(String, default="Pending")
class ParentDB(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String)
    father_name = Column(String)
    mother_name = Column(String)
    mobile = Column(String)
    email = Column(String)
    address = Column(String)
    occupation = Column(String)
    student_id = Column(Integer)