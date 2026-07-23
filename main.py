from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import json

app = FastAPI(title="Student Management System")


# -------------------------------
# Load JSON Data
# -------------------------------

with open("sample_data.json", "r") as file:
    students = json.load(file)


# -------------------------------
# Save JSON Data
# -------------------------------

def save_data():
    with open("sample_data.json", "w") as file:
        json.dump(students, file, indent=4)


# -------------------------------
# Pydantic Models
# -------------------------------

class Student(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=17)
    course: str
    email: EmailStr


class Marks(BaseModel):
    tamil: int
    english: int
    maths: int
    science: int
    social: int


class Fees(BaseModel):
    course_fee: float
    paid_fee: float


class Leave(BaseModel):
    total_leave: int
    used_leave: int


# -------------------------------
# Home API
# -------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management System API"
    }


# -------------------------------
# Get All Students
# -------------------------------

@app.get("/students")
def get_students(course: str = None):

    if course:

        filtered_students = [
            student
            for student in students
            if student["course"].lower() == course.lower()
        ]

        return filtered_students

    return students


# -------------------------------
# Get Student By ID
# -------------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )
# -------------------------------
# Add Student
# -------------------------------

@app.post("/students")
def add_student(student: Student):

    for s in students:
        if s["id"] == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students.append(student.model_dump())

    save_data()

    return {
        "message": "Student added successfully",
        "student": student
    }


# -------------------------------
# Update Student
# -------------------------------

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            students[index] = updated_student.model_dump()

            save_data()

            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )


# -------------------------------
# Delete Student
# -------------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            deleted_student = students.pop(index)

            save_data()

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )
# -------------------------------
# Dashboard Statistics
# -------------------------------

@app.get("/dashboard")
def dashboard():

    total_students = len(students)

    ai_students = len(
        [student for student in students if student["course"].lower() == "ai"]
    )

    ds_students = len(
        [student for student in students if student["course"].lower() == "data science"]
    )

    average_age = round(
        sum(student["age"] for student in students) / total_students, 2
    ) if total_students > 0 else 0

    return {
        "total_students": total_students,
        "ai_students": ai_students,
        "data_science_students": ds_students,
        "average_age": average_age
    }


# -------------------------------
# Calculate Marks
# -------------------------------

@app.post("/marks")
def calculate_marks(mark: Marks):

    total = (
        mark.tamil +
        mark.english +
        mark.maths +
        mark.science +
        mark.social
    )

    average = total / 5
    percentage = (total / 500) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "Fail"

    return {
        "Total": total,
        "Average": round(average, 2),
        "Percentage": round(percentage, 2),
        "Grade": grade
    }




