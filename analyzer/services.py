import requests
from django.core.cache import cache
from .skills import find_skills

API_URL = "https://remotive.com/api/remote-jobs"

def fetch_jobs_for_role(role, limit=30):
    """
    Fetch and cache public remote job listings. Cache key is role-specific.
    Remotive recommends no more than four requests per day.
    """
    key = "remotive_jobs_" + role.lower().replace(" ", "_")
    cached = cache.get(key)
    if cached is not None:
        return cached, None, True

    try:
        response = requests.get(
            API_URL,
            params={"search": role, "limit": limit},
            headers={"User-Agent": "SkillGapStudentProject/1.0"},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        jobs = payload.get("jobs", [])
        # Cache even an empty successful result to avoid repeated requests.
        cache.set(key, jobs, 21600)
        return jobs, None, False
    except (requests.RequestException, ValueError) as exc:
        return [], str(exc), False

def skills_from_job_descriptions(jobs):
    combined = " ".join(
        f"{job.get('title', '')} {job.get('description', '')} {job.get('category', '')}"
        for job in jobs
    )
    return find_skills(combined)
