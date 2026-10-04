import csv
import os


FILE_NAME = "applications.csv"


def save_application(job, status):

    file_exists = os.path.exists(FILE_NAME)

    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Company",
                "Job Title",
                "Location",
                "Match %",
                "Application URL",
                "Status"
            ])

        writer.writerow([
            job.get("date", ""),
            job.get("company", ""),
            job.get("title", ""),
            job.get("location", ""),
            job.get("match_score", ""),
            job.get("url", ""),
            status
        ])
