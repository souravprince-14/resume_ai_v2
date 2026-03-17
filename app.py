import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2

# 1. Configuration
st.set_page_config(page_title="Resume Matcher AI", page_icon="📄")

load_dotenv()  # load .env if present
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    st.warning(
        "GENAI_API_KEY is not set. Set the environment variable or create a `.env` file with GENAI_API_KEY=<your_key>."
    )

# -----------------------------
# Session state for button disabling
# -----------------------------
if "processing" not in st.session_state:
    st.session_state.processing = False

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
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def is_resume_like(text: str) -> bool:
    """Use Gemini to strictly classify whether the text looks like a resume/CV."""
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
                You are a strict classifier for resume detection.

                You will be given the content of a document.
                If it is a professional resume/CV (with things like work experience, skills, education, projects),
                reply with exactly: RESUME
                If it is anything else (cheat sheet, article, post, code, social media, some random text,etc.),
                reply with exactly: NOT_RESUME

                Document:
                {text[:4000]}
            """

    resp = model.generate_content(prompt)
    answer = resp.text.strip().upper()
    return answer == "RESUME"


def analyze_resume(resume_content, job_description):
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
    response = model.generate_content(prompt)
    return response.text


def run_analysis(uploaded_file, job_desc):
    mime_type = uploaded_file.type

    # Step 1: Validate file type
    if mime_type not in ALLOWED_RESUME_MIME_TYPES:
        st.error("❌ The uploaded file type is not supported. Please upload a PDF or TXT resume.")
        return

    # Step 2: Extract text content
    if mime_type == "application/pdf":
        content = extract_text_from_pdf(uploaded_file)
    elif mime_type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    else:
        st.error("❌ Unsupported file type. Please upload a PDF or TXT resume.")
        return

    # Step 3: Validate that the content actually looks like a resume
    if not is_resume_like(content):
        st.error(
            "❌ The uploaded document does not look like a resume. "
            "Please upload a proper resume (with your experience, skills, and education)."
        )
        return

    # Step 4: JD vs Resume analysis
    result = analyze_resume(content, job_desc)
    st.success("Analysis Complete!")
    st.markdown(result)


# 3. UI Layout
st.title("📄 Resume Matcher AI")
st.markdown("Upload your resume and job description to get AI-powered feedback.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or TXT resume", type=["pdf", "txt"])

with col2:
    st.subheader("2. Job Description")
    job_desc = st.text_area("Paste job description here", height=300)

# ---- BUTTON (no rerun magic) ----
if st.button(
    "Analyze Resume",
    type="primary",
    disabled=st.session_state.processing,
):
    if not uploaded_file or not job_desc:
        st.warning("Please provide both a resume and a job description.")
    else:
        st.session_state.processing = True
        with st.spinner("Analyzing resume..."):
            try:
                run_analysis(uploaded_file, job_desc)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                st.session_state.processing = False
