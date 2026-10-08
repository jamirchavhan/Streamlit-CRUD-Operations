import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

st.title("🎓 Student Management System")

st.header("➕ Add Student")

with st.form("add_student"):

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100)
    city = st.text_input("City")

    submit = st.form_submit_button("Add Student")

    if submit:

        if not name.strip() or not city.strip():
            st.error("Please fill all fields.")

        else:
            try:
                load_dotenv()
                DATABASE_URL = "postgresql://postgres:ehqLAElnOmwRu7Ix@db.ysnlxhjmzlhucbcgtdkh.supabase.co:5432/postgres"
                connection = psycopg2.connect(DATABASE_URL)

                cursor = connection.cursor()

                query = """
                    INSERT INTO students (name, age, city)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(
                    query,
                    (name.strip(), age, city.strip())
                )

                connection.commit()

                st.success("Student added successfully!")
                st.rerun()

            except mysql.connector.Error as e:
                st.error(f"Database error: {e}")

            finally:
                    cursor.close()
                    connection.close()


st.header("📋 Student List")

try:

    load_dotenv()
    DATABASE_URL = "postgresql://postgres:ehqLAElnOmwRu7Ix@db.ysnlxhjmzlhucbcgtdkh.supabase.co:5432/postgres"
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, city
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    header = st.columns([1, 3, 1, 3, 1, 1])

    header[0].write("**ID**")
    header[1].write("**Name**")
    header[2].write("**Age**")
    header[3].write("**City**")
    header[4].write("**Update**")
    header[5].write("**Delete**")

    st.divider()

    for student in students:

        student_id = student[0]
        name = student[1]
        age = student[2]
        city = student[3]

        row = st.columns([1, 3, 1, 3, 1, 1])

        row[0].write(student_id)
        row[1].write(name)
        row[2].write(age)
        row[3].write(city)

        if row[4].button(
            "✏️",
            key=f"update_{student_id}"
        ):
            st.session_state["edit_id"] = student_id
            st.rerun()

        if row[5].button(
            "🗑️",
            key=f"delete_{student_id}"
        ):

            try:
                load_dotenv()
                DATABASE_URL = "postgresql://postgres:ehqLAElnOmwRu7Ix@db.ysnlxhjmzlhucbcgtdkh.supabase.co:5432/postgres"
                connection = psycopg2.connect(DATABASE_URL)
                cursor = connection.cursor()

                cursor.execute(
                    "DELETE FROM students WHERE id = %s",
                    (student_id,)
                )

                connection.commit()

                cursor.close()
                connection.close()

                st.success(f"{name} deleted successfully!")
                st.rerun()

            except mysql.connector.Error as e:
                st.error(f"Database error: {e}")

except mysql.connector.Error as e:
    st.error(f"Database error: {e}")


if "edit_id" in st.session_state:

    edit_id = st.session_state["edit_id"]

    try:

        load_dotenv()
        DATABASE_URL = "postgresql://postgres:ehqLAElnOmwRu7Ix@db.ysnlxhjmzlhucbcgtdkh.supabase.co:5432/postgres"
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name, age, city
            FROM students
            WHERE id = %s
            """,
            (edit_id,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student:

            st.divider()
            st.subheader("✏️ Update Student")

            with st.form("update_form"):

                new_name = st.text_input(
                    "Name",
                    value=student[0]
                )

                new_age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=100,
                    value=student[1]
                )

                new_city = st.text_input(
                    "City",
                    value=student[2]
                )

                col1, col2 = st.columns(2)

                update = col1.form_submit_button(
                    "💾 Save Changes"
                )

                cancel = col2.form_submit_button(
                    "❌ Cancel"
                )

                if update:

                    load_dotenv()
                    DATABASE_URL = "postgresql://postgres:ehqLAElnOmwRu7Ix@db.ysnlxhjmzlhucbcgtdkh.supabase.co:5432/postgres"
                    connection = psycopg2.connect(DATABASE_URL)
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        UPDATE students
                        SET name = %s,
                            age = %s,
                            city = %s
                        WHERE id = %s
                        """,
                        (
                            new_name.strip(),
                            new_age,
                            new_city.strip(),
                            edit_id
                        )
                    )

                    connection.commit()

                    cursor.close()
                    connection.close()

                    del st.session_state["edit_id"]

                    st.success("Student updated successfully!")
                    st.rerun()

                if cancel:

                    del st.session_state["edit_id"]
                    st.rerun()

    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
