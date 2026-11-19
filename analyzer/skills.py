
import re
from urllib.parse import quote_plus
from pypdf import PdfReader


# --------------------------------------------------
# 1. SKILL ALIASES
# --------------------------------------------------

SKILL_ALIASES = {
    "python": ["python"],
    "django": ["django"],
    "flask": ["flask"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "react.js"],
    "angular": ["angular"],
    "node.js": ["node.js", "nodejs"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb"],
    "git": ["git", "github"],
    "rest api": ["rest api", "restful api"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "linux": ["linux"],
    "jenkins": ["jenkins"],
    "terraform": ["terraform"],
    "ci/cd": ["ci/cd", "continuous integration"],
    "machine learning": ["machine learning", "ml"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "ms excel"],
    "statistics": ["statistics", "statistical"],
    "data analysis": ["data analysis", "data analytics"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "cybersecurity": ["cybersecurity", "information security"],
    "networking": ["networking", "tcp/ip"],
    "firewalls": ["firewall", "firewalls"],
    "owasp": ["owasp"],
    "selenium": ["selenium"],
    "pytest": ["pytest"],
    "api testing": ["api testing", "postman"],
    "communication": ["communication"],
    "agile": ["agile", "scrum"],
}


# --------------------------------------------------
# 2. REQUIRED SKILLS FOR EACH JOB ROLE
# --------------------------------------------------

ROLE_SKILLS = {
    "Python Developer": [
        "python", "django", "sql", "git",
        "rest api", "pytest", "docker", "linux"
    ],

    "Django Developer": [
        "python", "django", "sql", "mysql",
        "rest api", "git", "docker", "pytest"
    ],

    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "typescript", "git", "rest api"
    ],

    "Full Stack Developer": [
        "html", "css", "javascript", "react",
        "python", "django", "sql", "git", "docker"
    ],

    "Data Analyst": [
        "sql", "excel", "power bi", "tableau",
        "python", "pandas", "statistics", "data analysis"
    ],

    "Data Scientist": [
        "python", "sql", "pandas", "numpy",
        "statistics", "machine learning",
        "scikit-learn", "tensorflow"
    ],

    "Cloud Engineer": [
        "aws", "azure", "linux", "networking",
        "docker", "kubernetes", "terraform", "ci/cd"
    ],

    "DevOps Engineer": [
        "linux", "docker", "kubernetes",
        "jenkins", "terraform", "aws", "git", "ci/cd"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity", "networking", "linux",
        "firewalls", "owasp", "python"
    ],

    "Java Developer": [
        "java", "sql", "git", "rest api",
        "docker", "jenkins"
    ],
}


# --------------------------------------------------
# 3. OFFICIAL LEARNING RESOURCES
# --------------------------------------------------

LEARNING_RESOURCES = {
    "python": "https://docs.python.org/3/tutorial/",
    "django": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
    "flask": "https://flask.palletsprojects.com/en/stable/tutorial/",
    "java": "https://dev.java/learn/",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "typescript": "https://www.typescriptlang.org/docs/",
    "html": "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "css": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "react": "https://react.dev/learn",
    "angular": "https://angular.dev/tutorials",
    "node.js": "https://nodejs.org/en/learn",
    "sql": "https://www.w3schools.com/sql/",
    "mysql": "https://dev.mysql.com/doc/",
    "postgresql": "https://www.postgresql.org/docs/",
    "mongodb": "https://www.mongodb.com/docs/",
    "git": "https://git-scm.com/doc",
    "rest api": "https://developer.mozilla.org/en-US/docs/Web/HTTP",
    "docker": "https://docs.docker.com/get-started/",
    "kubernetes": "https://kubernetes.io/docs/tutorials/",
    "aws": "https://aws.amazon.com/training/",
    "azure": "https://learn.microsoft.com/en-us/training/azure/",
    "gcp": "https://cloud.google.com/learn",
    "linux": "https://ubuntu.com/tutorials",
    "jenkins": "https://www.jenkins.io/doc/tutorials/",
    "terraform": "https://developer.hashicorp.com/terraform/tutorials",
    "ci/cd": "https://docs.github.com/en/actions",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "pandas": "https://pandas.pydata.org/docs/getting_started/",
    "numpy": "https://numpy.org/learn/",
    "power bi": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
    "tableau": "https://www.tableau.com/learn/training",
    "excel": "https://support.microsoft.com/en-us/excel",
    "statistics": "https://www.khanacademy.org/math/statistics-probability",
    "data analysis": "https://www.coursera.org/browse/data-science",
    "pytorch": "https://pytorch.org/tutorials/",
    "tensorflow": "https://www.tensorflow.org/tutorials",
    "scikit-learn": "https://scikit-learn.org/stable/tutorial/",
    "cybersecurity": "https://www.cisa.gov/resources-tools",
    "networking": "https://www.cisco.com/site/us/en/learn/training-certifications/index.html",
    "firewalls": "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/",
    "owasp": "https://owasp.org/www-project-top-ten/",
    "selenium": "https://www.selenium.dev/documentation/",
    "pytest": "https://docs.pytest.org/en/stable/getting-started.html",
    "api testing": "https://learning.postman.com/docs/introduction/overview/",
    "communication": "https://www.coursera.org/browse/business/leadership-and-management",
    "agile": "https://www.atlassian.com/agile",
}


# --------------------------------------------------
# 4. EXTRACT TEXT FROM RESUME PDF
# --------------------------------------------------

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)

    extracted_text = []

    for page in reader.pages:
        extracted_text.append(page.extract_text() or "")

    return "\n".join(extracted_text)


# --------------------------------------------------
# 5. IDENTIFY SKILLS FROM RESUME
# --------------------------------------------------

def find_skills(text):
    text = (text or "").lower()

    found = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<![a-z0-9+#.])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9+#.])"
            )

            if re.search(pattern, text):
                found.append(skill)
                break

    return sorted(set(found))


# --------------------------------------------------
# 6. GET REQUIRED SKILLS FOR SELECTED ROLE
# --------------------------------------------------

def role_skills(role):
    return ROLE_SKILLS.get(role, [])


# --------------------------------------------------
# 7. GET OFFICIAL LEARNING LINK
# --------------------------------------------------

def get_learning_link(skill):
    skill = skill.lower().strip()

    if skill in LEARNING_RESOURCES:
        return LEARNING_RESOURCES[skill]

    search_query = quote_plus(skill + " official documentation")

    return (
        "https://www.google.com/search?q="
        + search_query
    )


# --------------------------------------------------
# 8. GET YOUTUBE TUTORIAL LINK
# --------------------------------------------------

def get_youtube_link(skill):
    skill = skill.lower().strip()

    search_query = quote_plus(
        skill + " tutorial for beginners"
    )

    return (
        "https://www.youtube.com/results?search_query="
        + search_query
    )


# --------------------------------------------------
# 9. GET LEARNING RESOURCES FOR ALL MISSING SKILLS
# --------------------------------------------------

def get_missing_skill_resources(missing_skills):

    resources = []

    for skill in missing_skills:

        resources.append({
            "skill": skill,
            "link": get_learning_link(skill),
            "youtube_link": get_youtube_link(skill),
        })

    return resources
