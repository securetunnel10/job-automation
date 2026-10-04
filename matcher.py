# ==========================================
# IT SUPPORT JOB MATCHER
# ==========================================
#
# Purpose:
# - Jooble jobs ko user's IT Support profile
#   ke saath match karna
# - 0-100 relevance score generate karna
# - Strong IT Support jobs ko higher score dena
# - Completely unrelated jobs ko reduce karna
#
# ==========================================

import re


# ==========================================
# 1. IT SUPPORT SKILL GROUPS
# ==========================================

SKILL_GROUPS = {

    # --------------------------------------
    # IT SUPPORT / DESKTOP SUPPORT
    # --------------------------------------

    "it_support": [
        "it support",
        "it support executive",
        "it support engineer",
        "it support specialist",
        "it support technician",
        "it technician",
        "desktop support",
        "desktop support engineer",
        "desktop support technician",
        "technical support",
        "technical support engineer",
        "technical support executive",
        "helpdesk support",
        "help desk support",
        "it helpdesk",
        "it help desk",
        "system support",
        "system support engineer",
        "service desk",
        "it service desk"
    ],


    # --------------------------------------
    # WINDOWS
    # --------------------------------------

    "windows": [
        "windows",
        "windows 10",
        "windows 11",
        "windows installation",
        "windows troubleshooting",
        "windows support",
        "windows os"
    ],


    # --------------------------------------
    # HARDWARE
    # --------------------------------------

    "hardware": [
        "hardware",
        "hardware troubleshooting",
        "hardware support",
        "desktop hardware",
        "laptop hardware",
        "computer hardware",
        "hardware maintenance",
        "hardware issue",
        "hardware issues"
    ],


    # --------------------------------------
    # SOFTWARE
    # --------------------------------------

    "software": [
        "software",
        "software installation",
        "software troubleshooting",
        "software configuration",
        "software support",
        "application support",
        "application troubleshooting",
        "application installation"
    ],


    # --------------------------------------
    # NETWORKING
    # --------------------------------------

    "networking": [
        "networking",
        "network support",
        "network troubleshooting",
        "network administration",
        "lan",
        "wan",
        "tcp/ip",
        "tcp ip",
        "ip address",
        "dns",
        "dhcp",
        "wifi",
        "wi-fi",
        "router",
        "switch",
        "ethernet",
        "network issue",
        "network issues"
    ],


    # --------------------------------------
    # PRINTER
    # --------------------------------------

    "printer": [
        "printer",
        "printer support",
        "printer installation",
        "printer troubleshooting",
        "printer setup",
        "printing issues",
        "print support"
    ],


    # --------------------------------------
    # REMOTE SUPPORT
    # --------------------------------------

    "remote_support": [
        "remote desktop",
        "remote desktop support",
        "remote support",
        "remote assistance",
        "remote troubleshooting",
        "rdp",
        "anydesk",
        "teamviewer"
    ],


    # --------------------------------------
    # MS OFFICE
    # --------------------------------------

    "ms_office": [
        "ms office",
        "microsoft office",
        "microsoft word",
        "microsoft excel",
        "microsoft outlook",
        "word",
        "excel",
        "outlook"
    ],


    # --------------------------------------
    # TROUBLESHOOTING
    # --------------------------------------

    "troubleshooting": [
        "troubleshooting",
        "technical troubleshooting",
        "system troubleshooting",
        "hardware troubleshooting",
        "software troubleshooting",
        "issue resolution",
        "issue resolving",
        "problem solving",
        "incident resolution",
        "technical issue"
    ],


    # --------------------------------------
    # HELPDESK / TICKETING
    # --------------------------------------

    "helpdesk_ticketing": [
        "helpdesk",
        "help desk",
        "ticketing",
        "ticket management",
        "ticket resolution",
        "service desk",
        "it service desk",
        "incident management",
        "incident ticket",
        "support ticket"
    ],


    # --------------------------------------
    # ACTIVE DIRECTORY / USER MANAGEMENT
    # --------------------------------------

    "user_account_management": [
        "active directory",
        "active directory administration",
        "ad administration",
        "domain controller",
        "user account management",
        "user account creation",
        "user account",
        "user id creation",
        "user id",
        "account creation",
        "user access",
        "access management",
        "access provisioning",
        "user onboarding"
    ],


    # --------------------------------------
    # GOOGLE WORKSPACE
    # --------------------------------------

    "google_workspace": [
        "google workspace",
        "google admin",
        "google admin console",
        "google administration",
        "gmail administration",
        "google drive",
        "google docs",
        "google sheets",
        "google workspace administration"
    ],


    # --------------------------------------
    # ASSET MANAGEMENT
    # --------------------------------------

    "asset_management": [
        "asset management",
        "it asset management",
        "asset tracking",
        "asset inventory",
        "asset management system",
        "asset master",
        "asset master sheet",
        "asset register",
        "inventory management",
        "it inventory",
        "hardware inventory"
    ],


    # --------------------------------------
    # BUSINESS / WORKPLACE TOOLS
    # --------------------------------------

    "business_tools": [
        "timechamp",
        "looker studio",
        "leadsquared",
        "lead squared",
        "interakt",
        "tata tele",
        "tatatele"
    ],


    # --------------------------------------
    # SYSTEM ADMINISTRATION
    # --------------------------------------

    "system_administration": [
        "system administration",
        "system administrator",
        "system admin",
        "it administration",
        "server support",
        "system maintenance",
        "computer administration"
    ],


    # --------------------------------------
    # BIOS / COMMAND LINE
    # --------------------------------------

    "system_tools": [
        "bios",
        "bios setup",
        "command prompt",
        "cmd",
        "system configuration",
        "os installation",
        "operating system installation"
    ]
}


# ==========================================
# 2. STRONG JOB TITLE KEYWORDS
# ==========================================
#
# Agar job title directly IT Support related
# hai to extra score milega.
#
# ==========================================

STRONG_TITLE_KEYWORDS = [

    "it support",
    "it support executive",
    "it support engineer",
    "it support specialist",
    "it support technician",

    "desktop support",
    "desktop support engineer",
    "desktop support technician",

    "technical support",
    "technical support engineer",
    "technical support executive",

    "helpdesk",
    "help desk",

    "it technician",

    "system support",
    "system support engineer",

    "service desk",
    "it service desk"
]


# ==========================================
# 3. IRRELEVANT JOB KEYWORDS
# ==========================================
#
# Ye jobs ko completely delete nahi karta.
# Sirf penalty deta hai.
#
# Isliye agar description me kisi unrelated
# word ka accidental mention ho to job
# completely reject nahi hogi.
#
# ==========================================

IRRELEVANT_KEYWORDS = [

    "sales manager",
    "sales executive",

    "telecaller",
    "telecaller executive",

    "accountant",
    "chartered accountant",

    "hr manager",
    "human resources manager",
    "human resource executive",

    "digital marketing executive",
    "marketing manager",

    "content writer",

    "civil engineer",
    "mechanical engineer",
    "electrical engineer",

    "nurse",
    "doctor",
    "pharmacist",

    "lawyer",
    "legal advisor"
]


# ==========================================
# 4. NORMALIZE TEXT
# ==========================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower()

    # Convert common separators to spaces
    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = text.replace(".", " ")
    text = text.replace(",", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 5. KEYWORD MATCH
# ==========================================

def keyword_found(text, keyword):

    keyword = normalize_text(keyword)

    if not keyword:
        return False

    return keyword in text


# ==========================================
# 6. MATCH JOB
# ==========================================

def match_score(job_text):

    text = normalize_text(job_text)

    matched_groups = []
    matched_keywords = []


    # ======================================
    # CHECK EVERY SKILL GROUP
    # ======================================

    for group_name, keywords in SKILL_GROUPS.items():

        group_match = False

        for keyword in keywords:

            if keyword_found(text, keyword):

                group_match = True

                matched_keywords.append(keyword)

                break

        if group_match:

            matched_groups.append(group_name)


    # ======================================
    # BASE SCORE
    # ======================================

    total_groups = len(SKILL_GROUPS)

    if total_groups == 0:

        base_score = 0

    else:

        base_score = (
            len(matched_groups) / total_groups
        ) * 100


    # ======================================
    # STRONG IT SUPPORT BONUS
    # ======================================

    title_bonus = 0

    for keyword in STRONG_TITLE_KEYWORDS:

        if keyword_found(text, keyword):

            title_bonus = 15

            break


    # ======================================
    # IRRELEVANT JOB PENALTY
    # ======================================

    penalty = 0

    for keyword in IRRELEVANT_KEYWORDS:

        if keyword_found(text, keyword):

            penalty = 25

            break


    # ======================================
    # FINAL SCORE
    # ======================================

    final_score = base_score + title_bonus - penalty


    # Keep score between 0 and 100

    final_score = max(
        0,
        min(100, final_score)
    )


    final_score = round(final_score)


    # ======================================
    # RETURN RESULT
    # ======================================

    return final_score, matched_keywords
