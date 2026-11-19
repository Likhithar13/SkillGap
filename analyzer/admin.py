from django.contrib import admin
from .models import SkillAnalysis

@admin.register(SkillAnalysis)
class SkillAnalysisAdmin(admin.ModelAdmin):
    list_display = ("user", "target_role", "match_percentage", "jobs_checked", "created_at")
    list_filter = ("target_role", "created_at")
    search_fields = ("user__username", "target_role")
