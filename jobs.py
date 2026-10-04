import json
import os
import requests

from matcher import match_score


# ==============================
# LOAD CONFIG
# ==============================

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


# ==============================
# JOOBLE API
# ==============================

API_KEY = os.getenv("JOOBLE_API_KEY")

if not API_KEY:
    print("ERROR: JOOBLE_API_KEY secret is missing.")
    raise SystemExit(1)


API_URL = f"https://in.jooble.org/api/{API_KEY}"


# ==============================
# SEARCH JOOBLE
# ==============================

def search_jooble(keyword):

    payload = {
        "keywords": keyword,
        "location": "India",
        "page": 1
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    except Exception as e:

        print(f"Jooble search failed for '{keyword}': {e}")

        return []


# ==============================
# FILTER JOBS
# ==============================

def filter_jobs(jobs):

    suitable_jobs = []

    minimum_match = config["minimum_match"]

    for job in jobs:

        title = job.get("title", "")
        description = job.get("snippet", "")
        location = job.get("location", "")

        job_text = (
            title
            + " "
            + description
            + " "
            + location
        )

        score, matched_keywords = match_score(job_text)

        if score >= minimum_match:

            job["match_score"] = score
            job["matched_keywords"] = matched_keywords

            suitable_jobs.append(job)

    return suitable_jobs


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("===================================")
    print("JOB AUTOMATION STARTED")
    print("===================================")

    print("Target locations: India + Remote")

    print(
        "Minimum match:",
        config["minimum_match"],
        "%"
    )

    print()

    all_jobs = []

    keywords = config["keywords"]

    print("Searching Jooble...")

    for keyword in keywords:

        print(f"Searching: {keyword}")

        jobs = search_jooble(keyword)

        print(
            f"Found {len(jobs)} jobs for '{keyword}'"
        )

        all_jobs.extend(jobs)

    print()
    print("Total jobs collected:", len(all_jobs))

    # ==============================
    # REMOVE DUPLICATES
    # ==============================

    unique_jobs = {}

    for job in all_jobs:

        link = job.get("link")

        if link:
            unique_jobs[link] = job

    all_jobs = list(unique_jobs.values())

    print(
        "Unique jobs:",
        len(all_jobs)
    )

    # ==============================
    # MATCH JOBS
    # ==============================

    suitable_jobs = filter_jobs(all_jobs)

    print(
        "Matching jobs:",
        len(suitable_jobs)
    )

    print()
    print("===================================")
    print("MATCHING JOBS")
    print("===================================")

    if not suitable_jobs:

        print("No matching jobs found.")

    else:

        for number, job in enumerate(
            suitable_jobs,
            start=1
        ):

            print()
            print(f"JOB #{number}")

            print(
                "Title:",
                job.get("title", "N/A")
            )

            print(
                "Company:",
                job.get("company", "N/A")
            )

            print(
                "Location:",
                job.get("location", "N/A")
            )

            print(
                "Match:",
                job.get("match_score", 0),
                "%"
            )

            print(
                "Matched skills:",
                ", ".join(
                    job.get(
                        "matched_keywords",
                        []
                    )
                )
            )

            print(
                "Apply:",
                job.get("link", "N/A")
            )

            print("-----------------------------------")

    print()
    print("JOB AUTOMATION FINISHED")
