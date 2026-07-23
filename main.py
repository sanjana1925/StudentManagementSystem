from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List
import json

app = FastAPI(title="Student Management System")


# ----------------------------
# Load data from JSON
# ----------------------------
with open("sample_data.json", "r") as file:
    students = json.load(file)


# ----------------------------
# Pydantic Model
# ----------------------------
class Student(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=17)
    course: str
    email: EmailStr


# ----------------------------
# Home API
# ----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Student Management System API"}


# ----------------------------
# Get All Students
# ----------------------------
@app.get("/students")
def get_students():
    return students


# ----------------------------
# Get Student by ID
# ----------------------------
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


# ----------------------------
# Add Student
# ----------------------------
@app.post("/students")
def add_student(student: Student):

    for s in students:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="Student ID already exists")

    students.append(student.model_dump())

    with open("sample_data.json", "w") as file:
        json.dump(students, file, indent=4)

    return {"message": "Student added successfully"}


# ----------------------------
# Update Student
# ----------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            students[index] = updated_student.model_dump()

            with open("sample_data.json", "w") as file:
                json.dump(students, file, indent=4)

            return {"message": "Student updated successfully"}

    raise HTTPException(status_code=404, detail="Student not found")


# ----------------------------
# Delete Student
# ----------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            students.pop(index)

            with open("sample_data.json", "w") as file:
                json.dump(students, file, indent=4)

            return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")