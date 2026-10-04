KEYWORDS = [
    "it support",
    "desktop support",
    "technical support",
    "it support executive",
    "helpdesk support",
    "it helpdesk",
    "desktop support engineer",
    "technical support engineer",
    "windows",
    "hardware troubleshooting",
    "software installation",
    "software troubleshooting",
    "networking",
    "lan",
    "tcp/ip",
    "ip address",
    "dns",
    "wifi",
    "printer troubleshooting",
    "remote desktop",
    "ms office"
]


def match_score(job_text):

    text = job_text.lower()

    found = []

    for keyword in KEYWORDS:
        if keyword in text:
            found.append(keyword)

    score = round(
        (len(found) / len(KEYWORDS)) * 100
    )

    return score, found
