import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Search Student",
        "Update Student",
        "Delete Student"
    ]
)

# ---------------- Dashboard ----------------

if menu == "Dashboard":

    st.header("Dashboard")

    try:
        response = requests.get(f"{BASE_URL}/students")

        if response.status_code == 200:

            students = response.json()

            df = pd.DataFrame(students)

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Students", len(df))

            ai_count = len(df[df["course"] == "AI"])
            col2.metric("AI Students", ai_count)

            avg_age = round(df["age"].mean(), 2)
            col3.metric("Average Age", avg_age)

            st.dataframe(df, use_container_width=True)

    except:
        st.error("Backend is not running.")


# ---------------- Add Student ----------------

elif menu == "Add Student":

    st.header("Add Student")

    sid = st.number_input("ID", min_value=1)

    name = st.text_input("Name")

    age = st.number_input("Age", min_value=18)

    course = st.text_input("Course")

    email = st.text_input("Email")

    if st.button("Add Student"):

        data = {
            "id": sid,
            "name": name,
            "age": age,
            "course": course,
            "email": email
        }

        response = requests.post(
            f"{BASE_URL}/students",
            json=data
        )

        if response.status_code == 200:
            st.success("Student Added Successfully")
        else:
            st.error(response.json())


# ---------------- View Students ----------------

elif menu == "View Students":

    st.header("All Students")

    response = requests.get(f"{BASE_URL}/students")

    if response.status_code == 200:

        df = pd.DataFrame(response.json())

        st.dataframe(df, use_container_width=True)


# ---------------- Search Student ----------------

elif menu == "Search Student":

    st.header("Search Student")

    sid = st.number_input("Enter Student ID", min_value=1)

    if st.button("Search"):

        response = requests.get(f"{BASE_URL}/students/{sid}")

        if response.status_code == 200:

            st.json(response.json())

        else:

            st.error("Student Not Found")


# ---------------- Update Student ----------------

elif menu == "Update Student":

    st.header("Update Student")

    sid = st.number_input("Student ID", min_value=1)

    name = st.text_input("New Name")

    age = st.number_input("New Age", min_value=18)

    course = st.text_input("New Course")

    email = st.text_input("New Email")

    if st.button("Update"):

        data = {
            "id": sid,
            "name": name,
            "age": age,
            "course": course,
            "email": email
        }

        response = requests.put(
            f"{BASE_URL}/students/{sid}",
            json=data
        )

        if response.status_code == 200:

            st.success("Student Updated Successfully")

        else:

            st.error("Student Not Found")


# ---------------- Delete Student ----------------

elif menu == "Delete Student":

    st.header("Delete Student")

    sid = st.number_input("Student ID", min_value=1)

    if st.button("Delete"):

        response = requests.delete(f"{BASE_URL}/students/{sid}")

        if response.status_code == 200:

            st.success("Student Deleted Successfully")

        else:

            st.error("Student Not Found")