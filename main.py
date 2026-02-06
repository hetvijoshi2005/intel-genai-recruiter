import streamlit as st
import pandas as pd
from utils.pdf_loader import extract_text_from_pdf
from utils.scaledown import compress_resume
from utils.gemini_client import analyze_candidate, generate_bias_report

# Page Config
st.set_page_config(page_title="AI Recruitment Agent", layout="wide")

# Title and Header
st.title("🤖 Intel GenAI Agent: Smart Recruitment Screening")
st.markdown("### Powered by Gemini 1.5 Flash & ScaleDown.ai")

# --- INITIALIZE SESSION STATE ---
# This keeps your data alive even when you click buttons
if 'results' not in st.session_state:
    st.session_state['results'] = None

# Sidebar: Inputs
with st.sidebar:
    st.header("1. Job Setup")
    job_description = st.text_area("Paste Job Description (JD)", height=300, placeholder="Paste the JD here...")
    
    st.header("2. Candidate Upload")
    uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    
    run_analysis = st.button("🚀 Run Screening Agent")

# --- LOGIC: PROCESS FILES ---
if run_analysis and job_description and uploaded_files:
    
    temp_results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process each file
    for i, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}...")
        
        # 1. Extract Text
        raw_text = extract_text_from_pdf(file)
        
        # 2. Compress Text (ScaleDown.ai)
        if len(raw_text) > 2000:
            status_text.text(f"Compressing {file.name} with ScaleDown.ai...")
            processed_text = compress_resume(raw_text)
        else:
            processed_text = raw_text

        # 3. Analyze (Gemini Brain)
        status_text.text(f"Analyzing {file.name} with Gemini...")
        ai_response = analyze_candidate(processed_text, job_description)
        
        # Add filename
        ai_response["filename"] = file.name
        temp_results.append(ai_response)
        
        # Update progress
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Analysis Complete!")
    
    # SAVE TO SESSION STATE
    st.session_state['results'] = temp_results

# --- LOGIC: DISPLAY RESULTS ---
# Only show this section if results exist in Session State
if st.session_state['results']:
    results = st.session_state['results'] # Retrieve from state
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # 1. High-Level Leaderboard
    st.divider()
    st.subheader("🏆 Candidate Leaderboard")
    
    display_cols = ["candidate_name", "match_score", "summary", "filename"]
    st.dataframe(
        df[display_cols].sort_values(by="match_score", ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # 2. Detailed Breakdown
    st.divider()
    st.subheader("🧐 Detailed Analysis")
    
    # Check if we have valid candidate names, else use "Candidate 1", "Candidate 2"
    tab_labels = [c.get("candidate_name", f"Candidate {i+1}") for i, c in enumerate(results)]
    candidate_tabs = st.tabs(tab_labels)
    
    for tab, candidate in zip(candidate_tabs, results):
        with tab:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Match Score", value=f"{candidate['match_score']}%")
                
                st.markdown("#### ✅ Matched Skills")
                st.write(", ".join(candidate.get("technical_skills_match", [])))
                
                st.markdown("#### ❌ Missing Skills")
                st.write(", ".join(candidate.get("missing_skills", [])))

            with col2:
                # Bias Audit Section
                st.markdown("#### ⚖️ Bias Audit Report")
                bias_data = candidate.get("bias_audit", {"flagged": False, "details": "N/A"})
                
                if bias_data.get("flagged"):
                    st.error(f"⚠️ Potential Bias Detected: {bias_data.get('details')}")
                else:
                    st.success("✅ No major bias triggers detected.")
                
                # Interview Questions
                st.markdown("#### 🎤 Recommended Interview Questions")
                for q in candidate.get("interview_questions", []):
                    st.info(f"- {q}")

    # 3. Download Report (Now Safe)
    st.divider()
    report_text = generate_bias_report(results)
    st.download_button(
        label="📄 Download Bias Audit Report",
        data=report_text,
        file_name="bias_audit_report.md",
        mime="text/markdown"
    )

elif run_analysis:
    st.warning("Please upload resumes and provide a Job Description.")

# Footer
st.markdown("---")
st.caption("Built for Intel GenAI for GenZ Challenge | Team Hetvi")