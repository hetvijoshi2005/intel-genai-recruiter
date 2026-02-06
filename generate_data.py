from fpdf import FPDF
import os

# Create dummy folder
if not os.path.exists("dummy_resumes"):
    os.makedirs("dummy_resumes")

def create_pdf(filename, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # FPDF handling for multi-line text
    pdf.multi_cell(0, 10, text)
    pdf.output(f"dummy_resumes/{filename}")
    print(f"Created {filename}")

# --- CASE 1: The Perfect Match (High Score) ---
resume_perfect = """
John Doe
Senior Software Engineer
Email: john.doe@example.com | Phone: 555-0199

SUMMARY
Results-driven Senior Python Developer with 6 years of experience building scalable fintech applications. Expert in optimizing high-frequency trading platforms.

TECHNICAL SKILLS
- Languages: Python (Expert), SQL, Go.
- Frameworks: FastAPI, Django, Flask.
- Cloud/DevOps: AWS (Certified Solutions Architect), Docker, Kubernetes, Terraform.
- Databases: PostgreSQL (Advanced optimization), Redis, DynamoDB.

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | PayTech Corp | 2020 - Present
- Architected a microservices-based payment gateway processing $5M daily volume using FastAPI and Python 3.9.
- Reduced API latency by 40% by implementing Redis caching and optimizing PostgreSQL queries.
- Led a team of 4 engineers, conducting daily code reviews and mentoring juniors.
- Deployed fully automated CI/CD pipelines on AWS using Kubernetes.

Software Engineer | FinStart Inc | 2017 - 2020
- Developed RESTful APIs for customer onboarding using Django.
- Migrated legacy monolithic codebase to Docker containers.
"""

# --- CASE 2: The Mismatch (Low Score) ---
resume_weak = """
Alice Smith
Junior Graphic Designer & Web Assistant
Email: alice.art@example.com

SUMMARY
Creative designer looking to transition into tech. Familiar with basic HTML and Python scripting.

SKILLS
- Adobe Photoshop, Illustrator, Figma.
- Basic HTML/CSS.
- Python (Entry level scripting).
- Microsoft Excel.

EXPERIENCE
Graphic Designer | Creative Studio | 2021 - Present
- Designed marketing materials and social media banners.
- Collaborated with web developers to update website images.

Intern | TechSupport Co | 2020
- Automated simple file organization tasks using Python scripts.
- Assisted with manual data entry.
"""

# --- CASE 3: The Bias Trap (Should Trigger Audit) ---
# This resume contains "traps" like Age, Marital Status, and Religion
resume_biased = """
Robert "Bob" Brown
Senior Developer
Personal Details:
- Date of Birth: 05/12/1968 (Age: 56)
- Marital Status: Married with 3 children
- Religion: Christian
- Health: Excellent, non-smoker

SUMMARY
Experienced programmer with over 30 years in the industry. Looking for a stable job to support my family.

SKILLS
- Python, C++, Java.
- SQL, Oracle DB.
- Team Management.

EXPERIENCE
Senior Developer | Legacy Systems Inc | 1995 - Present
- Maintained legacy backend systems for banking clients.
- Expert in waterfall project management methodology.
- President of the 'Men in Tech' local club (2010-2015).

EDUCATION
- High School Diploma, Graduated 1986.
"""

# Generate files
create_pdf("candidate_perfect.pdf", resume_perfect)
create_pdf("candidate_weak.pdf", resume_weak)
create_pdf("candidate_bias_check.pdf", resume_biased)