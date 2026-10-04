def apply_to_job(job):

    if not job.get("automation_allowed"):
        return {
            "status": "manual",
            "message": "Automatic submission is not allowed for this source."
        }

    # Officially permitted application API/endpoint
    # will be connected here.

    return {
        "status": "submitted",
        "message": "Application submitted through an allowed mechanism."
    }
