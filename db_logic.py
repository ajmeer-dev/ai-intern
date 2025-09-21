import streamlit as st
from db_connection import get_db_connection

def get_jobs_by_filters(skill=None, location=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if skill:
            query += " AND FIND_IN_SET(%s, required_skills)"
            params.append(skill)

        if location:
            query += " AND location = %s"
            params.append(location)

        cursor.execute(query, tuple(params))
        jobs = cursor.fetchall()

        cursor.close()
        conn.close()
        return jobs

    except Exception as e:
        st.error(f"Database error: {e}")
        return None
