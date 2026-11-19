# SkillGap — AI-Based Skill Gap Analyzer

A complete Django student project with a polished responsive UI, PDF resume skill extraction, role-based skill comparison, saved reports, and live remote job listings from the Remotive public API.

## Features
- User registration, login and logout
- Student dashboard and analysis history
- PDF resume upload (up to 5 MB)
- Keyword-based skill extraction from PDF resumes
- Ten target job roles with editable baseline skill profiles
- Skill match percentage, matched skills and missing skills
- Personalized learning roadmap
- Live job search using Remotive's public API
- Six-hour server-side cache to avoid excessive API requests
- Django admin
- SQLite database by default (no database server setup required)
- Responsive Bootstrap-based UI

## Requirements
- Python 3.10+
- Internet connection for installing packages and calling the live job API

## Windows setup (PowerShell)
Open the terminal in the folder containing `manage.py`.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell blocks activation, run this for the current terminal only:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```
You can also skip activation and use `venv\Scripts\python.exe` for commands.

## First use
1. Register a normal user account on the website.
2. Log in and click **New skill analysis**.
3. Choose a target role.
4. Upload a text-based PDF resume (optional, maximum 5 MB).
5. Click **Analyze my skill gap**.
6. Review your match score, skills you have, missing skills, roadmap and real job listings.

## Live API integration
Endpoint: `https://remotive.com/api/remote-jobs`

The app calls the API server-side with a role search and limit, reads job titles and descriptions, and extracts skill keywords from those descriptions. Results are cached for six hours. The Remotive API is a remote-job feed; its listings can be delayed by 24 hours. The app credits Remotive and links each listing to its original Remotive URL.

Remotive's terms require attribution and a link back to each listing. Do not republish these listings to third-party job boards. See:
- https://remotive.com/remote-jobs/api
- https://github.com/remotive-com/remote-jobs-api

The app also has a built-in role skill profile. This means the report can still be generated if the external API is temporarily unavailable. The interface warns when live API results are unavailable.

## Important accuracy note
This is a student-project prototype. Resume parsing and skill identification use transparent keyword matching, not a trained AI model. The match score is an indicative comparison against the configured role profile plus skills detected in current API job descriptions. It is not a hiring prediction. Edit `analyzer/skills.py` to customize the skills and roles.

## Admin
Go to http://127.0.0.1:8000/admin/ and sign in with the superuser created above.

## Deployment notes
- Set `DJANGO_DEBUG=False`
- Set a strong `DJANGO_SECRET_KEY`
- Set `DJANGO_ALLOWED_HOSTS` to your deployed domain
- Configure persistent media storage for uploaded resumes
- Configure a production database (e.g. PostgreSQL)
- Run `python manage.py collectstatic`
- Use Gunicorn or your host's supported WSGI server

This starter uses SQLite for easiest local setup. Do not deploy with DEBUG enabled or the sample secret key.
