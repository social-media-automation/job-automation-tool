import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# -----------------------------
# Function: Fetch Jobs
# -----------------------------
def fetch_indeed_jobs(query="software engineer", location="Pakistan"):
    url = f"https://pk.indeed.com/jobs?q={query}&l={location}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    jobs = []

    for job in soup.find_all("div", class_="job_seen_beacon"):
        title = job.find("h2")
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        link = job.find("a")

        jobs.append({
            "Title": title.text.strip() if title else "N/A",
            "Company": company.text.strip() if company else "N/A",
            "Location": location.text.strip() if location else "N/A",
            "Link": "https://pk.indeed.com" + link.get("href") if link else "N/A",
            "Verified": "Yes" if "indeed" in url else "No"
        })

    return pd.DataFrame(jobs)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Job Finder", layout="wide")

st.title("🔍 Indeed Job Finder (Basic Version)")

query = st.text_input("Enter Job Title", "Software Engineer")
location = st.text_input("Enter Location", "Pakistan")

if st.button("Search Jobs"):
    with st.spinner("Fetching jobs..."):
        df = fetch_indeed_jobs(query, location)
        time.sleep(1)

    st.success(f"{len(df)} Jobs Found")

    if not df.empty:
        st.dataframe(df)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            "jobs.csv",
            "text/csv"
        )
    else:
        st.warning("No jobs found")
