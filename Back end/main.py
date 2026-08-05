from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn

from database import engine, Base, SessionLocal
from models import StudentDB, TeacherDB, AttendanceDB, FeesDB, SubjectDB, UserDB, MarksDB, ClassDB, HomeworkDB, ExamDB, TimetableDB, LeaveDB, SalaryDB, ParentDB
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_role
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


class Student(BaseModel):

    id: int
    name: str
    student_class: str


class Teacher(BaseModel):
    id: int
    name: str
    subject: str


class Attendance(BaseModel):
    student_id: int
    date: str
    status: str

class Fees(BaseModel):
    student_id: int
    amount: int
    month: str
    status: str


class Subject(BaseModel):
    id: int
    name: str
    teacher_id: int


class User(BaseModel):
    id: int
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Marks(BaseModel):
    student_id: int
    subject: str
    marks: int
class Class(BaseModel):
    class_name: str
    section: str
    teacher_id: int

class Homework(BaseModel):
    class_name: str
    subject: str
    title: str
    due_date: str

class Exam(BaseModel):
    exam_name: str
    class_name: str
    exam_date: str
    total_marks: int

class Timetable(BaseModel):
    class_name: str
    day: str
    subject: str
    start_time: str
    end_time: str
    teacher_id: int

class Leave(BaseModel):
    employee_name: str
    leave_type: str
    from_date: str
    to_date: str
    reason: str

class Salary(BaseModel):
    employee_name: str
    employee_id: str
    designation: str
    month: str
    basic_salary: float
    bonus: float
    deduction: float
class Parent(BaseModel):
    parent_name: str
    father_name: str
    mother_name: str
    mobile: str
    email: str
    address: str
    occupation: str
    student_id: int

@app.get("/")
def home():
    return {
        "message": "Welcome to Lumiora AI",
        "project": "AI Powered School ERP"
    }


# ---------------- STUDENT APIs ----------------

@app.get("/students")
def get_students():
    db = SessionLocal()
    students = db.query(StudentDB).all()
    db.close()
    return students


@app.post("/students")
def add_student(student: Student):
    db = SessionLocal()

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        student_class=student.student_class
    )

    db.add(new_student)
    db.commit()
    db.close()

    return {
        "message": "Student added successfully to database"
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    db = SessionLocal()

    existing_student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not existing_student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.student_class = student.student_class

    db.commit()
    db.refresh(existing_student)

    db.close()

    return {
        "message": "Student updated successfully",
        "student": existing_student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()
    db.close()

    return {
        "message": "Student deleted successfully"
    }

# ---------------- TEACHER APIs ----------------

@app.get("/teachers")
def get_teachers():
    db = SessionLocal()
    teachers = db.query(TeacherDB).all()
    db.close()
    return teachers


@app.post("/teachers")
def add_teacher(teacher: Teacher):
    db = SessionLocal()

    new_teacher = TeacherDB(
        id=teacher.id,
        name=teacher.name,
        subject=teacher.subject
    )

    db.add(new_teacher)
    db.commit()
    db.close()

    return {
        "message": "Teacher added successfully"
    }
@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, teacher: Teacher):
    db = SessionLocal()

    db_teacher = db.query(TeacherDB).filter(
        TeacherDB.id == teacher_id
    ).first()

    if not db_teacher:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    db_teacher.name = teacher.name
    db_teacher.subject = teacher.subject

    db.commit()
    db.close()

    return {
        "message": "Teacher updated successfully"
    }


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    db = SessionLocal()

    teacher = db.query(TeacherDB).filter(
        TeacherDB.id == teacher_id
    ).first()

    if not teacher:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    db.delete(teacher)
    db.commit()
    db.close()

    return {
        "message": "Teacher deleted successfully"
    }

    # ---------------- ATTENDANCE APIs ----------------
# ---------------- ATTENDANCE APIs ----------------

@app.get("/attendance")
def get_attendance():
    db = SessionLocal()
    attendance = db.query(AttendanceDB).all()
    db.close()
    return attendance

@app.post("/attendance")
def add_attendance(attendance: Attendance):
    db = SessionLocal()

    new_attendance = AttendanceDB(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    db.close()

    return {
        "message": "Attendance added successfully",
        "id": new_attendance.id
    }


@app.put("/attendance/{attendance_id}")
def update_attendance(attendance_id: int, attendance: Attendance):
    db = SessionLocal()

    db_attendance = db.query(AttendanceDB).filter(
        AttendanceDB.id == attendance_id
    ).first()

    if not db_attendance:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    db_attendance.student_id = attendance.student_id
    db_attendance.date = attendance.date
    db_attendance.status = attendance.status

    db.commit()
    db.close()

    return {
        "message": "Attendance updated successfully"
    }


@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int):
    db = SessionLocal()

    attendance = db.query(AttendanceDB).filter(
        AttendanceDB.id == attendance_id
    ).first()

    if not attendance:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    db.delete(attendance)
    db.commit()
    db.close()

    return {
        "message": "Attendance deleted successfully"
    }

# ---------------- FEES APIs ----------------

@app.get("/fees")
def get_fees():
    db = SessionLocal()

    fees = db.query(FeesDB).all()

    db.close()

    return fees


@app.post("/fees")
def add_fees(fees: Fees):
    db = SessionLocal()

    new_fees = FeesDB(
        student_id=fees.student_id,
        amount=fees.amount,
        month=fees.month,
        status=fees.status
    )

    db.add(new_fees)
    db.commit()
    db.refresh(new_fees)
    db.close()

    return {
        "message": "Fees added successfully",
        "id": new_fees.id
    }


@app.put("/fees/{fees_id}")
def update_fees(fees_id: int, fees: Fees):
    db = SessionLocal()

    db_fees = db.query(FeesDB).filter(
        FeesDB.id == fees_id
    ).first()

    if not db_fees:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fees not found"
        )

    db_fees.student_id = fees.student_id
    db_fees.amount = fees.amount
    db_fees.month = fees.month
    db_fees.status = fees.status

    db.commit()
    db.close()

    return {
        "message": "Fees updated successfully"
    }

@app.delete("/fees/{fees_id}")
def delete_fees(fees_id: int):
    db = SessionLocal()

    fees = db.query(FeesDB).filter(
        FeesDB.id == fees_id
    ).first()

    if not fees:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fees not found"
        )

    db.delete(fees)
    db.commit()
    db.close()

    return {
        "message": "Fees deleted successfully"
    }



# ---------------- SUBJECT APIs ----------------

@app.get("/student/subjects")
def student_subjects(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    subjects = db.query(SubjectDB).all()

    db.close()

    return {
        "student": current_user["username"],
        "subjects": [
            {
                "name": item.name,
                "teacher_id": item.teacher_id
            }
            for item in subjects
        ]
    }


@app.post("/subjects")
def add_subject(subject: Subject):
    db = SessionLocal()

    new_subject = SubjectDB(
        id=subject.id,
        name=subject.name,
        teacher_id=subject.teacher_id
    )

    db.add(new_subject)
    db.commit()
    db.close()

    return {
        "message": "Subject added successfully"
    }


@app.put("/subjects/{subject_id}")
def update_subject(subject_id: int, subject: Subject):
    db = SessionLocal()

    db_subject = db.query(SubjectDB).filter(
        SubjectDB.id == subject_id
    ).first()

    if not db_subject:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db_subject.name = subject.name
    db_subject.teacher_id = subject.teacher_id

    db.commit()
    db.close()

    return {
        "message": "Subject updated successfully"
    }

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int):
    db = SessionLocal()

    subject = db.query(SubjectDB).filter(
        SubjectDB.id == subject_id
    ).first()

    if not subject:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db.delete(subject)
    db.commit()
    db.close()

    return {
        "message": "Subject deleted successfully"
    }

@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users


@app.post("/register")
def register(user: User):
    db = SessionLocal()

    existing_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing_user:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = UserDB(
        id=user.id,
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {
        "message": "User registered successfully"
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.username == form_data.username
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "username": user.username,
        "role": user.role
    })

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/admin/dashboard")
def admin_dashboard(
    current_user: dict = Depends(require_role("admin"))
):
    return {
        "message": "Welcome Admin",
        "user": current_user
    }


@app.post("/admin/fees")
def add_fees(
    current_user: dict = Depends(require_role("admin"))
):
    db = SessionLocal()

    fees = FeesDB(
        student_id=1,
        amount=50000,
        month="August",
        status="Pending"
    )

    db.add(fees)
    db.commit()
    db.refresh(fees)

    db.close()

    return {
        "message": "Fees added successfully",
        "id": fees.id
    }

@app.post("/admin/subjects")
def add_subject(
    current_user: dict = Depends(require_role("admin"))
):
    db = SessionLocal()

    subject = SubjectDB(
        name="Mathematics",
        teacher_id=1
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    db.close()

    return {
        "message": "Subject added successfully",
        "id": subject.id
    }

@app.get("/teacher/dashboard")
def teacher_dashboard(
    current_user: dict = Depends(require_role("teacher"))
):
    return {
        "message": "Welcome Teacher",
        "user": current_user
    }


@app.get("/student/dashboard")
def student_dashboard(
    current_user: dict = Depends(require_role("student"))
):
    return {
        "message": "Welcome Student",
        "user": current_user
    }


@app.get("/student/attendance")
def student_attendance(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    attendance = db.query(AttendanceDB).filter(
        AttendanceDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "attendance": [
            {
                "date": item.date,
                "status": item.status
            }
            for item in attendance
        ]
    }

@app.get("/student/fees")
def student_fees(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    fees = db.query(FeesDB).filter(
        FeesDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "fees": [
            {
                "month": item.month,
                "amount": item.amount,
                "status": item.status
            }
            for item in fees
        ]
    }

@app.get("/student/subjects")
def student_subjects(
    current_user: dict = Depends(require_role("student"))
):
    return {
        "student": current_user["username"],
        "subjects": [
            {
                "name": "Mathematics",
                "teacher": "Ravi"
            },
            {
                "name": "Science",
                "teacher": "Anitha"
            }
        ]
    }

@app.get("/student/progress")
def student_progress(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    marks = db.query(MarksDB).filter(
        MarksDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "progress": [
            {
                "subject": item.subject,
                "marks": item.marks
            }
            for item in marks
        ]
    }

@app.get("/teacher/subjects")
def teacher_subjects(
    current_user: dict = Depends(require_role("teacher"))
):
    return {
        "teacher": current_user["username"],
        "subjects": [
            "Mathematics",
            "Science"
        ]
    }
@app.post("/teacher/attendance")
def mark_attendance(
    current_user: dict = Depends(require_role("teacher"))
):
    db = SessionLocal()

    attendance = AttendanceDB(
        student_id=1,
        date="2026-08-01",
        status="Present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    db.close()

    return {
        "message": "Attendance saved successfully",
        "id": attendance.id
    }

@app.post("/teacher/marks")
def upload_marks(
    marks: Marks,
    current_user: dict = Depends(require_role("teacher"))
):
    db = SessionLocal()

    new_marks = MarksDB(
        student_id=marks.student_id,
        subject=marks.subject,
        marks=marks.marks
    )

    db.add(new_marks)
    db.commit()
    db.refresh(new_marks)

    db.close()

    return {
        "message": "Marks saved successfully",
        "id": new_marks.id
        }
@app.get("/marks")
def get_marks():
    db = SessionLocal()

    marks = db.query(MarksDB).all()

    db.close()

    return marks


@app.put("/marks/{marks_id}")
def update_marks(marks_id: int, marks: Marks):
    db = SessionLocal()

    db_marks = db.query(MarksDB).filter(
        MarksDB.id == marks_id
    ).first()

    if not db_marks:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Marks not found"
        )

    db_marks.student_id = marks.student_id
    db_marks.subject = marks.subject
    db_marks.marks = marks.marks

    db.commit()
    db.close()

    return {
        "message": "Marks updated successfully"
    }

@app.delete("/marks/{marks_id}")
def delete_marks(marks_id: int):
    db = SessionLocal()

    marks = db.query(MarksDB).filter(
        MarksDB.id == marks_id
    ).first()

    if not marks:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Marks not found"
        )

    db.delete(marks)
    db.commit()
    db.close()

    return {
        "message": "Marks deleted successfully"
    }


@app.post("/classes")
def add_class(class_data: Class):
    db = SessionLocal()

    new_class = ClassDB(
        class_name=class_data.class_name,
        section=class_data.section,
        teacher_id=class_data.teacher_id
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    db.close()

    return {
        "message": "Class added successfully",
        "id": new_class.id
    }

@app.get("/classes")
def get_classes():
    db = SessionLocal()

    classes = db.query(ClassDB).all()

    db.close()

    return classes


@app.put("/classes/{class_id}")
def update_class(class_id: int, class_data: Class):
    db = SessionLocal()

    db_class = db.query(ClassDB).filter(
        ClassDB.id == class_id
    ).first()

    if not db_class:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

        db_class.class_name = class_data.class_name
    db_class.section = class_data.section
    db_class.teacher_id = class_data.teacher_id

    db.commit()
    db.close()

    return {
        "message": "Class updated successfully"
    }


@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    db = SessionLocal()

    db_class = db.query(ClassDB).filter(
        ClassDB.id == class_id
    ).first()

    if not db_class:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    db.delete(db_class)
    db.commit()
    db.close()

    return {
        "message": "Class deleted successfully"
    }


@app.post("/homework")
def add_homework(homework: Homework):
    db = SessionLocal()

    new_homework = HomeworkDB(
        class_name=homework.class_name,
        subject=homework.subject,
        title=homework.title,
        due_date=homework.due_date
    )

    db.add(new_homework)
    db.commit()
    db.refresh(new_homework)
    db.close()

    return {
        "message": "Homework added successfully",
        "id": new_homework.id
    }

@app.get("/homework")
def get_homework():
    db = SessionLocal()

    homework = db.query(HomeworkDB).all()

    db.close()

    return homework


@app.put("/homework/{homework_id}")
def update_homework(homework_id: int, homework: Homework):
    db = SessionLocal()

    db_homework = db.query(HomeworkDB).filter(
        HomeworkDB.id == homework_id
    ).first()

    if not db_homework:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    db_homework.class_name = homework.class_name
    db_homework.subject = homework.subject
    db_homework.title = homework.title
    db_homework.due_date = homework.due_date

    db.commit()
    db.close()

    return {
        "message": "Homework updated successfully"
    }


@app.delete("/homework/{homework_id}")
def delete_homework(homework_id: int):
    db = SessionLocal()

    db_homework = db.query(HomeworkDB).filter(
        HomeworkDB.id == homework_id
    ).first()

    if not db_homework:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    db.delete(db_homework)
    db.commit()
    db.close()

    return {
        "message": "Homework deleted successfully"
    }

@app.post("/exams")
def add_exam(exam: Exam):
    db = SessionLocal()

    new_exam = ExamDB(
        exam_name=exam.exam_name,
        class_name=exam.class_name,
        exam_date=exam.exam_date,
        total_marks=exam.total_marks
    )

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    db.close()

    return {
        "message": "Exam added successfully",
        "id": new_exam.id
    }

@app.get("/exams")
def get_exams():
    db = SessionLocal()

    exams = db.query(ExamDB).all()

    db.close()

    return exams

@app.put("/exams/{exam_id}")
def update_exam(exam_id: int, exam: Exam):
    db = SessionLocal()

    db_exam = db.query(ExamDB).filter(
        ExamDB.id == exam_id
    ).first()

    if not db_exam:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    db_exam.exam_name = exam.exam_name
    db_exam.class_name = exam.class_name
    db_exam.exam_date = exam.exam_date
    db_exam.total_marks = exam.total_marks

    db.commit()
    db.close()

    return {
        "message": "Exam updated successfully"
    }


@app.delete("/exams/{exam_id}")
def delete_exam(exam_id: int):
    db = SessionLocal()

    db_exam = db.query(ExamDB).filter(
        ExamDB.id == exam_id
    ).first()

    if not db_exam:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    db.delete(db_exam)
    db.commit()
    db.close()

    return {
        "message": "Exam deleted successfully"
    }

@app.post("/timetable")
def add_timetable(timetable: Timetable):
    db = SessionLocal()

    new_timetable = TimetableDB(
        class_name=timetable.class_name,
        day=timetable.day,
        subject=timetable.subject,
        start_time=timetable.start_time,
        end_time=timetable.end_time,
        teacher_id=timetable.teacher_id
    )

    db.add(new_timetable)
    db.commit()
    db.refresh(new_timetable)
    db.close()

    return {
        "message": "Timetable added successfully",
        "id": new_timetable.id
    }

@app.get("/timetable")
def get_timetable():
    db = SessionLocal()

    timetable = db.query(TimetableDB).all()

    db.close()

    return timetable

@app.put("/timetable/{timetable_id}")
def update_timetable(timetable_id: int, timetable: Timetable):
    db = SessionLocal()

    db_timetable = db.query(TimetableDB).filter(
        TimetableDB.id == timetable_id
    ).first()

    if not db_timetable:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Timetable not found"
        )

    db_timetable.class_name = timetable.class_name
    db_timetable.day = timetable.day
    db_timetable.subject = timetable.subject
    db_timetable.start_time = timetable.start_time
    db_timetable.end_time = timetable.end_time
    db_timetable.teacher_id = timetable.teacher_id

    db.commit()
    db.close()

    return {
        "message": "Timetable updated successfully"
    }


@app.delete("/timetable/{timetable_id}")
def delete_timetable(timetable_id: int):
    db = SessionLocal()

    timetable = db.query(TimetableDB).filter(
        TimetableDB.id == timetable_id
    ).first()

    if not timetable:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Timetable not found"
        )

    db.delete(timetable)
    db.commit()
    db.close()

    return {
        "message": "Timetable deleted successfully"
    }


@app.post("/leave")
def apply_leave(leave: Leave):
    ...
    db = SessionLocal()

    new_leave = LeaveDB(
        employee_name=leave.employee_name,
        leave_type=leave.leave_type,
        from_date=leave.from_date,
        to_date=leave.to_date,
        reason=leave.reason,
        status="Pending"
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    db.close()

    return {
        "message": "Leave applied successfully",
        "id": new_leave.id
    }

@app.get("/leave")
def get_leaves():
    db = SessionLocal()

    leaves = db.query(LeaveDB).all()

    db.close()

    return leaves


@app.put("/leave/{leave_id}")
def update_leave_status(leave_id: int, status: str):
    db = SessionLocal()

    leave = db.query(LeaveDB).filter(
        LeaveDB.id == leave_id
    ).first()

    if not leave:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.status = status

    db.commit()
    db.refresh(leave)
    db.close()

    return {
        "message": "Leave status updated successfully"
    }

@app.delete("/leave/{leave_id}")
def delete_leave(leave_id: int):
    db = SessionLocal()

    leave = db.query(LeaveDB).filter(
        LeaveDB.id == leave_id
    ).first()

    if not leave:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    db.delete(leave)
    db.commit()
    db.close()

    return {
        "message": "Leave deleted successfully"
    }

@app.post("/salary")
def add_salary(salary: Salary):
    db = SessionLocal()

    net_salary = (
        salary.basic_salary +
        salary.bonus -
        salary.deduction
    )

    new_salary = SalaryDB(
        employee_name=salary.employee_name,
        employee_id=salary.employee_id,
        designation=salary.designation,
        month=salary.month,
        basic_salary=salary.basic_salary,
        bonus=salary.bonus,
        deduction=salary.deduction,
        net_salary=net_salary,
        payment_status="Pending"
    )

    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    db.close()

    return {
        "message": "Salary added successfully",
        "id": new_salary.id
    }

@app.get("/salary")
def get_salaries():
    db = SessionLocal()

    salaries = db.query(SalaryDB).all()

    db.close()

    return salaries

@app.get("/salary")
def get_salaries():
    db = SessionLocal()

    salaries = db.query(SalaryDB).all()

    db.close()

    return salaries


@app.put("/salary/{salary_id}")
def update_salary_status(salary_id: int, payment_status: str):
    db = SessionLocal()

    salary = db.query(SalaryDB).filter(
        SalaryDB.id == salary_id
    ).first()

    if not salary:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Salary record not found"
        )

    salary.payment_status = payment_status

    db.commit()
    db.refresh(salary)
    db.close()

    return {
        "message": "Salary status updated successfully"
    }

@app.delete("/salary/{salary_id}")
def delete_salary(salary_id: int):
    db = SessionLocal()

    salary = db.query(SalaryDB).filter(
        SalaryDB.id == salary_id
    ).first()

    if not salary:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Salary record not found"
        )

    db.delete(salary)
    db.commit()
    db.close()

    return {
        "message": "Salary deleted successfully"
    }

@app.post("/parents")
def add_parent(parent: Parent):
    db = SessionLocal()

    new_parent = ParentDB(
        parent_name=parent.parent_name,
        father_name=parent.father_name,
        mother_name=parent.mother_name,
        mobile=parent.mobile,
        email=parent.email,
        address=parent.address,
        occupation=parent.occupation,
        student_id=parent.student_id
    )

    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    db.close()

    return {
        "message": "Parent added successfully",
        "id": new_parent.id
    }

@app.get("/parents/{parent_id}")
def get_parent(parent_id: int):
    db = SessionLocal()

    parent = db.query(ParentDB).filter(
        ParentDB.id == parent_id
    ).first()

    db.close()

    if not parent:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    return parent


@app.put("/parents/{parent_id}")
def update_parent(parent_id: int, parent: Parent):
    db = SessionLocal()

    existing_parent = db.query(ParentDB).filter(
        ParentDB.id == parent_id
    ).first()

    if not existing_parent:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    existing_parent.parent_name = parent.parent_name
    existing_parent.father_name = parent.father_name
    existing_parent.mother_name = parent.mother_name
    existing_parent.mobile = parent.mobile
    existing_parent.email = parent.email
    existing_parent.address = parent.address
    existing_parent.occupation = parent.occupation
    existing_parent.student_id = parent.student_id

    db.commit()
    db.refresh(existing_parent)
    db.close()

    return {
        "message": "Parent updated successfully"
    }

@app.get("/dashboard")
def dashboard():
    db = SessionLocal()

    total_students = db.query(StudentDB).count()
    total_teachers = db.query(TeacherDB).count()
    total_parents = db.query(ParentDB).count()
    total_subjects = db.query(SubjectDB).count()
    total_classes = db.query(ClassDB).count()

    pending_leaves = db.query(LeaveDB).filter(
        LeaveDB.status == "Pending"
    ).count()

    pending_salary = db.query(SalaryDB).filter(
        SalaryDB.payment_status == "Pending"
    ).count()

    db.close()

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_parents": total_parents,
        "total_subjects": total_subjects,
        "total_classes": total_classes,
        "pending_leaves": pending_leaves,
        "pending_salary": pending_salary
    }
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )