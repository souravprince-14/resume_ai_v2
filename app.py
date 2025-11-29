import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PyPDF2
import io

# 1. Configuration
load_dotenv()  # load .env if present
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    # Warn in the UI but allow the app to load; analysis will fail without a key.
    st.warning("GENAI_API_KEY is not set. Set the environment variable or create a `.env` file with GENAI_API_KEY=<your_key>.")

st.set_page_config(page_title="Resume Matcher AI", page_icon="📄")

# -----------------------------
# Allowed resume MIME types
# -----------------------------
ALLOWED_RESUME_MIME_TYPES = [
    "application/pdf",  # PDF
    "text/plain",       # TXT
]

# 2. Helper Functions
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_content, job_description, mime_type):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert Career Coach. Compare the provided Resume against the Job Description.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME CONTENT:
    {resume_content}
    
    Please provide a detailed report in Markdown:
    1. Match Score (0-100)
    2. Missing Keywords
    3. Recommended Changes to bullet points
    """
    
    parts = [prompt]
    response = model.generate_content(parts)
    return response.text

# 3. UI Layout
st.title("📄 Resume Matcher AI")
st.markdown("Upload your resume and job description to get AI-powered feedback.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    # 🚫 Only allow proper resume docs (PDF, TXT)
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

with col2:
    st.subheader("2. Job Description")
    job_desc = st.text_area("Paste job description here", height=300)

if st.button("Analyze Resume", type="primary"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing resume..."):
            try:
                # Original MIME type from uploader
                mime_type = uploaded_file.type

                # 🔒 Validate it is a resume-type document
                if mime_type not in ALLOWED_RESUME_MIME_TYPES:
                    st.error("❌ The uploaded file is not a resume. Please upload a proper resume document (PDF or TXT).")
                    st.stop()

                # Process file
                if mime_type == "application/pdf":
                    content = extract_text_from_pdf(uploaded_file)
                elif mime_type == "text/plain":
                    content = uploaded_file.read().decode("utf-8")
                else:
                    # Extra safety (should not hit because of validation above)
                    st.error("❌ Unsupported file type. Please upload a proper resume document (PDF or TXT).")
                    st.stop()

                # Call Gemini
                result = analyze_resume(content, job_desc, "text/plain")
                
                st.success("Analysis Complete!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please provide both a resume and a job description.")
