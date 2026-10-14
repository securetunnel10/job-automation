
# ==========================================
# JOB AUTOMATION
# JOOBLE + REMOTIVE + RESUME MATCHING + TRACKER
# ==========================================

import json
import os
import re
from html import unescape
from html.parser import HTMLParser

import requests

from matcher import match_score
from apply import create_tracker, process_job, job_already_tracked


# ==========================================
# LOAD CONFIG
# ==========================================

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

MINIMUM_MATCH = config.get("minimum_match", 35)

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")
JOOBLE_API_URL = (
    f"https://in.jooble.org/api/{JOOBLE_API_KEY}"
    if JOOBLE_API_KEY
    else None
)

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


# ==========================================
# HTML DESCRIPTION CLEANER
# ==========================================

class HTMLTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.parts.append(text)


def clean_html(value):
    parser = HTMLTextParser()
    parser.feed(value or "")
    return re.sub(r"\s+", " ", unescape(" ".join(parser.parts))).strip()


# ==========================================
# SEARCH JOOBLE
# ==========================================

def search_jooble(keyword):
    if not JOOBLE_API_URL:
        print("WARNING: JOOBLE_API_KEY is missing.")
        return []

    payload = {
        "keywords": keyword,
        "location": "India",
        "page": 1
    }

    try:
        response = requests.post(
            JOOBLE_API_URL,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        for job in jobs:
            job["source"] = "Jooble"

        return jobs

    except Exception as error:
        print(f"Jooble search failed for '{keyword}': {error}")
        return []


# ==========================================
# SEARCH REMOTIVE
# No API key required
# ==========================================

def search_remotive():
    print("Searching Remotive remote jobs...")

    try:
        response = requests.get(
            REMOTIVE_API_URL,
            timeout=45,
            headers={"User-Agent": "ITJobSearchPersonal/1.0"}
        )
        response.raise_for_status()

        data = response.json()
        remote_jobs = data.get("jobs", [])
        normalized_jobs = []

        for item in remote_jobs:
            description = clean_html(item.get("description", ""))

            location = (
                item.get("candidate_required_location")
                or "Remote - eligibility to be checked"
            )

            normalized_jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": location,
                "snippet": description[:6000],
                "link": item.get("url", ""),
                "source": "Remotive",
                "job_type": item.get("job_type", ""),
                "salary": item.get("salary", ""),
                "publication_date": item.get("publication_date", ""),
                "remotive_id": item.get("id", "")
            })

        print(f"Remotive returned {len(normalized_jobs)} remote jobs.")
        return normalized_jobs

    except Exception as error:
        print(f"Remotive search failed: {error}")
        return []


# ==========================================
# RESUME MATCHING
# ==========================================

def filter_jobs(jobs):
    suitable_jobs = []

    for job in jobs:
        title = str(job.get("title", ""))
        description = str(
            job.get("snippet", job.get("description", ""))
        )
        location = str(job.get("location", ""))
        company = str(job.get("company", ""))

        job_text = " ".join([
            title,
            description,
            location,
            company
        ])

        score, matched_keywords = match_score(job_text)

        if score >= MINIMUM_MATCH:
            job["match_score"] = score
            job["matched_keywords"] = matched_keywords
            suitable_jobs.append(job)

    return suitable_jobs


# ==========================================
# DEDUPLICATE JOBS
# ==========================================

def remove_duplicates(jobs):
    unique_jobs = {}
    missing_link_count = 0

    for job in jobs:
        link = str(job.get("link", "")).strip()

        if not link:
            missing_link_count += 1
            continue

        # Keep the original listing URL for each source.
        unique_jobs[link] = job

    if missing_link_count:
        print(f"Skipped {missing_link_count} jobs without links.")

    return list(unique_jobs.values())


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    print("=" * 50)
    print("JOB AUTOMATION STARTED")
    print("=" * 50)
    print("Target: India + eligible remote jobs")
    print("Minimum match:", MINIMUM_MATCH, "%")
    print()

    create_tracker()

    # --------------------------------------
    # 1. Search Jooble
    # --------------------------------------

    all_jobs = []

    if JOOBLE_API_KEY:
        keywords = config.get("keywords", [])

        print("Searching Jooble...")

        for keyword in keywords:
            print(f"Searching: {keyword}")
            jobs = search_jooble(keyword)
            print(f"Found {len(jobs)} jobs for '{keyword}'")
            all_jobs.extend(jobs)
    else:
        print("Jooble skipped: API key is missing.")

    # --------------------------------------
    # 2. Search Remotive
    # --------------------------------------

    remotive_jobs = search_remotive()
    all_jobs.extend(remotive_jobs)

    print()
    print("Total jobs collected:", len(all_jobs))

    # --------------------------------------
    # 3. Remove duplicates
    # --------------------------------------

    all_jobs = remove_duplicates(all_jobs)
    print("Unique jobs:", len(all_jobs))

    # --------------------------------------
    # 4. Match jobs to your resume
    # --------------------------------------

    suitable_jobs = filter_jobs(all_jobs)

    # Highest match first
    suitable_jobs.sort(
        key=lambda job: job.get("match_score", 0),
        reverse=True
    )

    print("Matching jobs:", len(suitable_jobs))
    print()

    # --------------------------------------
    # 5. Display matching jobs
    # --------------------------------------

    print("=" * 50)
    print("MATCHING JOBS")
    print("=" * 50)

    for number, job in enumerate(suitable_jobs, start=1):
        print()
        print(f"JOB #{number}")
        print("Title:", job.get("title", "N/A"))
        print("Company:", job.get("company", "N/A"))
        print("Location:", job.get("location", "N/A"))
        print("Source:", job.get("source", "Unknown"))
        print("Match:", job.get("match_score", 0), "%")
        print("Apply:", job.get("link", "N/A"))
        print("Status: MANUAL_REQUIRED")
        print("-" * 40)

    # --------------------------------------
    # 6. Save jobs to tracker
    # --------------------------------------

    print()
    print("UPDATING APPLICATION TRACKER")

    new_jobs = 0
    already_tracked = 0

    for job in suitable_jobs:
        link = job.get("link", "")

        if not link:
            continue

        if job_already_tracked(link):
            already_tracked += 1
            print("Already tracked:", job.get("title", "N/A"))
        else:
            process_job(job)
            new_jobs += 1

    # --------------------------------------
    # 7. Summary
    # --------------------------------------

    print()
    print("=" * 50)
    print("JOB AUTOMATION FINISHED")
    print("Sources searched: Jooble + Remotive")
    print("Jobs collected:", len(all_jobs))
    print("Matching jobs:", len(suitable_jobs))
    print("New jobs added:", new_jobs)
    print("Already tracked:", already_tracked)
    print("=" * 50)
