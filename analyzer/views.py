
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import strip_tags

from .forms import RegisterForm, AnalysisForm
from .models import SkillAnalysis
from .skills import (
    extract_text_from_pdf,
    find_skills,
    role_skills,
    get_missing_skill_resources,
)
from .services import fetch_jobs_for_role, skills_from_job_descriptions


def home(request):
    return render(request, "analyzer/home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account is ready. Let's analyze your skills."
            )
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "analyzer/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "analyzer/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    analyses = SkillAnalysis.objects.filter(user=request.user)[:5]
    latest = analyses.first()

    return render(request, "analyzer/dashboard.html", {
        "analyses": analyses,
        "latest": latest,
        "total": SkillAnalysis.objects.filter(user=request.user).count(),
    })


@login_required
def analyze(request):
    if request.method == "POST":
        form = AnalysisForm(request.POST, request.FILES)

        if form.is_valid():
            role = form.cleaned_data["target_role"]
            resume = form.cleaned_data.get("resume")
            extracted = []

            if resume:
                try:
                    extracted = find_skills(
                        extract_text_from_pdf(resume)
                    )
                except Exception:
                    messages.error(
                        request,
                        "We could not read this PDF. Try a text-based PDF resume."
                    )
                    return render(
                        request,
                        "analyzer/analyze.html",
                        {"form": form}
                    )

            jobs, api_error, was_cached = fetch_jobs_for_role(role)
            job_skills = skills_from_job_descriptions(jobs)
            baseline = role_skills(role)

            # Combine built-in role skills and job description skills.
            required = sorted(set(baseline) | set(job_skills))

            matched = sorted(set(extracted) & set(required))
            missing = sorted(set(required) - set(extracted))

            percentage = (
                round((len(matched) / len(required)) * 100)
                if required else 0
            )

            analysis = SkillAnalysis.objects.create(
                user=request.user,
                target_role=role,
                resume=resume,
                extracted_skills=extracted,
                required_skills=required,
                missing_skills=missing,
                matched_skills=matched,
                match_percentage=percentage,
                jobs_checked=len(jobs),
            )

            if api_error:
                messages.warning(
                    request,
                    "Live job API could not be reached. We used the built-in role skill profile for this analysis."
                )

            return redirect("results", pk=analysis.pk)

    else:
        form = AnalysisForm()

    return render(request, "analyzer/analyze.html", {"form": form})


@login_required
def results(request, pk):
    analysis = get_object_or_404(
        SkillAnalysis,
        pk=pk,
        user=request.user
    )

    jobs, api_error, was_cached = fetch_jobs_for_role(
        analysis.target_role
    )

    # Generate official learning and YouTube links for missing skills.
    missing_skill_resources = get_missing_skill_resources(
        analysis.missing_skills
    )

    return render(request, "analyzer/results.html", {
        "analysis": analysis,
        "jobs": jobs[:6],
        "api_error": api_error,
        "was_cached": was_cached,
        "missing_skill_resources": missing_skill_resources,
    })


@login_required
def history(request):
    analyses = SkillAnalysis.objects.filter(user=request.user)

    return render(
        request,
        "analyzer/history.html",
        {"analyses": analyses}
    )

