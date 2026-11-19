from django.db import models
from django.contrib.auth.models import User

class SkillAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skill_analyses")
    target_role = models.CharField(max_length=120)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    extracted_skills = models.JSONField(default=list)
    required_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    matched_skills = models.JSONField(default=list)
    match_percentage = models.PositiveSmallIntegerField(default=0)
    jobs_checked = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.target_role} ({self.match_percentage}%)"
