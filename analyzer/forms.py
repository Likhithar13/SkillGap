from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

class AnalysisForm(forms.Form):
    ROLE_CHOICES = [
        ("Python Developer", "Python Developer"),
        ("Django Developer", "Django Developer"),
        ("Frontend Developer", "Frontend Developer"),
        ("Full Stack Developer", "Full Stack Developer"),
        ("Data Analyst", "Data Analyst"),
        ("Data Scientist", "Data Scientist"),
        ("Cloud Engineer", "Cloud Engineer"),
        ("DevOps Engineer", "DevOps Engineer"),
        ("Cybersecurity Analyst", "Cybersecurity Analyst"),
        ("Java Developer", "Java Developer"),
    ]
    target_role = forms.ChoiceField(choices=ROLE_CHOICES)
    resume = forms.FileField(
        required=False,
        help_text="Upload a PDF resume (maximum 5 MB)."
    )

    def clean_resume(self):
        file = self.cleaned_data.get("resume")
        if file:
            if not file.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Please upload a PDF file.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("The PDF must be 5 MB or smaller.")
        return file
