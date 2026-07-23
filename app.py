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
    "Select Option",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Search Student",
        "Update Student",
        "Delete Student",
        "Filter Students",
        "Calculate Marks"
    ]
)

# ===========================
# Dashboard
# ===========================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    try:

        response = requests.get(f"{BASE_URL}/dashboard")

        if response.status_code == 200:

            data = response.json()

            col1, col2 = st.columns(2)

            col3, col4 = st.columns(2)

            with col1:
                st.metric(
                    "Total Students",
                    data["total_students"]
                )

            with col2:
                st.metric(
                    "AI Students",
                    data["ai_students"]
                )

            with col3:
                st.metric(
                    "Data Science Students",
                    data["data_science_students"]
                )

            with col4:
                st.metric(
                    "Average Age",
                    data["average_age"]
                )

            st.divider()

            response = requests.get(f"{BASE_URL}/students")

            df = pd.DataFrame(response.json())

            st.subheader("Student Records")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("Students by Course")

            course_count = (
                df["course"]
                .value_counts()
            )

            st.bar_chart(course_count)

    except:

        st.error("FastAPI Backend is not running.")
# ===========================
# Add Student
# ===========================

elif menu == "Add Student":

    st.header("➕ Add Student")

    with st.form("add_student_form"):

        sid = st.number_input(
            "Student ID",
            min_value=1,
            step=1
        )

        name = st.text_input("Student Name")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            step=1
        )

        course = st.selectbox(
            "Course",
            [
                "AI",
                "Data Science",
                "Python",
                "Machine Learning",
                "Cyber Security",
                "Cloud Computing",
                "Web Development"
            ]
        )

        email = st.text_input("Email")

        submit = st.form_submit_button("Add Student")

    if submit:

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

            st.success("Student Added Successfully ✅")

            st.json(response.json())

        else:

            try:
                st.error(response.json()["detail"])
            except:
                st.error("Unable to add student.")


# ===========================
# View Students
# ===========================

elif menu == "View Students":

    st.header("📋 View All Students")

    response = requests.get(
        f"{BASE_URL}/students"
    )

    if response.status_code == 200:

        students = response.json()

        if len(students) == 0:

            st.warning("No Students Available.")

        else:

            df = pd.DataFrame(students)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name="students.csv",
                mime="text/csv"
            )

    else:

        st.error("Unable to fetch students.")
# ===========================
# Search Student
# ===========================

elif menu == "Search Student":

    st.header("🔍 Search Student")

    sid = st.number_input(
        "Enter Student ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):

        response = requests.get(
            f"{BASE_URL}/students/{sid}"
        )

        if response.status_code == 200:

            student = response.json()

            st.success("Student Found")

            st.json(student)

        else:

            st.error("Student Not Found")


# ===========================
# Update Student
# ===========================

elif menu == "Update Student":

    st.header("✏️ Update Student")

    sid = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    if st.button("Load Student"):

        response = requests.get(
            f"{BASE_URL}/students/{sid}"
        )

        if response.status_code == 200:

            st.session_state.student = response.json()

        else:

            st.error("Student Not Found")

    if "student" in st.session_state:

        student = st.session_state.student

        with st.form("update_form"):

            name = st.text_input(
                "Name",
                value=student["name"]
            )

            age = st.number_input(
                "Age",
                min_value=18,
                value=student["age"]
            )

            course = st.selectbox(
                "Course",
                [
                    "AI",
                    "Data Science",
                    "Python",
                    "Machine Learning",
                    "Cyber Security",
                    "Cloud Computing",
                    "Web Development"
                ],
                index=[
                    "AI",
                    "Data Science",
                    "Python",
                    "Machine Learning",
                    "Cyber Security",
                    "Cloud Computing",
                    "Web Development"
                ].index(student["course"])
            )

            email = st.text_input(
                "Email",
                value=student["email"]
            )

            submit = st.form_submit_button(
                "Update Student"
            )

        if submit:

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

                del st.session_state.student

            else:

                st.error("Unable to Update Student")


# ===========================
# Delete Student
# ===========================

elif menu == "Delete Student":

    st.header("🗑 Delete Student")

    sid = st.number_input(
        "Enter Student ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Student"):

        response = requests.delete(
            f"{BASE_URL}/students/{sid}"
        )

        if response.status_code == 200:

            st.success("Student Deleted Successfully")

        else:

            st.error("Student Not Found")
# ===========================
# Filter Students
# ===========================

elif menu == "Filter Students":

    st.header("📚 Filter Students")

    course = st.selectbox(
        "Select Course",
        [
            "AI",
            "Data Science",
            "Python",
            "Machine Learning",
            "Cyber Security",
            "Cloud Computing",
            "Web Development"
        ]
    )

    if st.button("Filter"):

        response = requests.get(
            f"{BASE_URL}/students",
            params={"course": course}
        )

        if response.status_code == 200:

            students = response.json()

            if len(students) == 0:

                st.warning("No Students Found")

            else:

                df = pd.DataFrame(students)

                st.dataframe(
                    df,
                    use_container_width=True
                )

        else:

            st.error("Unable to Fetch Students")


# ===========================
# Calculate Marks
# ===========================

elif menu == "Calculate Marks":

    st.header("📝 Marks Calculator")

    tamil = st.number_input("Tamil", 0, 100)
    english = st.number_input("English", 0, 100)
    maths = st.number_input("Mathematics", 0, 100)
    science = st.number_input("Science", 0, 100)
    social = st.number_input("Social", 0, 100)

    if st.button("Calculate Marks"):

        data = {
            "tamil": tamil,
            "english": english,
            "maths": maths,
            "science": science,
            "social": social
        }

        response = requests.post(
            f"{BASE_URL}/marks",
            json=data
        )

        if response.status_code == 200:

            result = response.json()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total", result["Total"])

            with col2:
                st.metric("Average", result["Average"])

            col3, col4 = st.columns(2)

            with col3:
                st.metric("Percentage", f'{result["Percentage"]}%')

            with col4:
                st.metric("Grade", result["Grade"])

        else:

            st.error("Calculation Failed")
