import json
from matcher import match_score


with open("config.json", "r") as file:
    config = json.load(file)


def filter_jobs(jobs):

    suitable_jobs = []

    for job in jobs:

        title = job.get("title", "")
        description = job.get("description", "")
        location = job.get("location", "")

        job_text = (
            title + " " +
            description + " " +
            location
        )

        score, matched_keywords = match_score(job_text)

        if score >= config["minimum_match"]:

            job["match_score"] = score
            job["matched_keywords"] = matched_keywords

            suitable_jobs.append(job)

    return suitable_jobs


if __name__ == "__main__":

    print("Job automation started.")

    print("Target locations: India + Remote")

    print(
        "Minimum match:",
        config["minimum_match"],
        "%"
    )
