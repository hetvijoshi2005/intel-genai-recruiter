# 🤖 RecruitAI: Intelligent Recruitment Screening Agent
> **Submitted for: Intel GenAI for GenZ Challenge**

RecruitAI is a high-performance, automated candidate screening platform designed to optimize the hiring process. It leverages **ScaleDown.ai** for token-efficient resume compression and **Gemini 2.5 Flash** for intelligent analysis, bias detection, and ranking.

## 🚀 Key Features
* **📉 Smart Compression (ScaleDown.ai):** Compresses 10+ page resumes by ~80% without losing critical context, enabling high-volume screening at low latency.
* **⚖️ Bias Guard Audit:** Automatically detects and flags potential bias triggers (age, gender, marital status) to ensure fair hiring practices.
* **🎯 Contextual Scoring:** Matches candidates against Job Descriptions (JD) with specific skill-gap analysis.
* **📝 Automated Outreach:** Generates interview questions tailored to the candidate's missing skills.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Optimization:** ScaleDown.ai API (Model: `gemini-2.5-flash`)
* **Reasoning Engine:** Google Gemini 2.5 Flash
* **Data Processing:** Pandas & PyPDF

## ⚙️ Setup & Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/hetvijoshi2005/intel-genai-recruiter.git](https://github.com/hetvijoshi2005/intel-genai-recruiter.git)
    cd intel-genai-recruiter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Create a `.env` file in the root directory:
    ```ini
    GEMINI_API_KEY=your_google_api_key_here
    SCALEDOWN_API_KEY=your_scaledown_api_key_here
    ```

4.  **Run the Application:**
    ```bash
    streamlit run main.py
    ```

## 📸 Usage Workflow
1.  Paste the **Job Description** in the sidebar.
2.  Upload candidate resumes (PDF format).
3.  Click **"Run Screening Agent"**.
4.  View the **Leaderboard**, analyze the **Bias Report**, and download the audit.

---
*Built by Team Hetvi for the Intel GenAI Hackathon 2026.*