# ==========================================
# JOB APPLICATION TRACKER
# ==========================================

import csv
import os
from datetime import datetime


TRACKER_FILE = "applications.csv"


# ==========================================
# CREATE TRACKER FILE
# ==========================================

def create_tracker():

    if not os.path.exists(TRACKER_FILE):

        with open(
            TRACKER_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Job Title",
                "Company",
                "Location",
                "Match Score",
                "Matched Skills",
                "Apply Link",
                "Source",
                "Status"
            ])


# ==========================================
# CHECK EXISTING JOB
# ==========================================

def job_already_tracked(apply_link):

    if not os.path.exists(TRACKER_FILE):
        return False

    with open(
        TRACKER_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("Apply Link") == apply_link:

                return True

    return False


# ==========================================
# SAVE JOB
# ==========================================

def save_job(job):

    apply_link = job.get("link", "")

    if not apply_link:
        return False

    # Don't save duplicate jobs
    if job_already_tracked(apply_link):

        return False

    with open(
        TRACKER_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            job.get(
                "title",
                "N/A"
            ),

            job.get(
                "company",
                "N/A"
            ),

            job.get(
                "location",
                "N/A"
            ),

            job.get(
                "match_score",
                0
            ),

            ", ".join(
                job.get(
                    "matched_keywords",
                    []
                )
            ),

            apply_link,

            "Jooble",

            "MANUAL_REQUIRED"
        ])

    return True


# ==========================================
# PROCESS MATCHING JOB
# ==========================================

def process_job(job):

    saved = save_job(job)

    if saved:

        print(
            "Added to application tracker:",
            job.get("title", "N/A")
        )

        print(
            "Status: MANUAL_REQUIRED"
        )

        print(
            "Apply:",
            job.get("link", "N/A")
        )

        print()

    else:

        print(
            "Already tracked:",
            job.get("title", "N/A")
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    create_tracker()

    print("Application tracker ready.")
