import streamlit as st
from db_logic import get_jobs_by_filters
from pdf_utils import extract_text_from_pdf, extract_skills_from_text

def main():
    st.set_page_config(page_title="Job Search by Skill and Location", layout="wide")
    st.title("💼 Job Search by Resume (PDF) or Manual Entry")

    st.markdown(
        """
        <style>
        .job-container {
            background-color: #121212;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .job-title {
            color: #00acee;
            font-weight: 700;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .job-detail {
            font-size: 16px;
            margin-bottom: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Upload Resume
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

    # Optional manual filters
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("📍 Enter location to search for (optional):")
    with col2:
        skill_override = st.text_input("🛠️ Enter skill manually (optional, overrides resume):")

    search_button = st.button("🔎 Search Jobs")

    if search_button:
        if uploaded_file or skill_override or location:
            st.info("🔍 Searching for jobs...")

            if uploaded_file:
                text = extract_text_from_pdf(uploaded_file)
                skills = extract_skills_from_text(text)
                st.success(f"✅ Extracted skills from resume: {', '.join(skills) if skills else 'None'}")
            else:
                skills = []

            # Use manual skill if entered
            if skill_override:
                skills = [skill_override.strip()]

            jobs_found = []
            for skill in skills:
                filtered_jobs = get_jobs_by_filters(skill=skill, location=location)
                if filtered_jobs:
                    jobs_found.extend(filtered_jobs)

            # Remove duplicates by job ID or title
            unique_jobs = {job['title'] + job['company']: job for job in jobs_found}.values()

            if not unique_jobs:
                st.warning("🚫 No jobs found with the given criteria.")
            else:
                for job in unique_jobs:
                    job_html = f"""
                    <div class="job-container">
                        <div class="job-title">{job.get('title', 'N/A')} at {job.get('company', 'N/A')}</div>
                        <div class="job-detail"><strong>Location:</strong> {job.get('location', 'N/A')}</div>
                        <div class="job-detail"><strong>Job Type:</strong> {job.get('job_type', 'N/A')}</div>
                        <div class="job-detail"><strong>Salary:</strong> {job.get('salary', 'N/A')}</div>
                        <div class="job-detail"><strong>Required Skills:</strong> {job.get('required_skills', 'N/A')}</div>
                    </div>
                    """
                    st.markdown(job_html, unsafe_allow_html=True)
        else:
            st.info("📌 Please upload a resume or enter at least one filter.")

if __name__ == "__main__":
    main()
