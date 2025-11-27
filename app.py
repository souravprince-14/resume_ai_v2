import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import PyPDF2
import io

# 1. Configuration
# Ensure you have GOOGLE_API_KEY in your environment variables
genai.configure(api_key='AIzaSyAgBEI_Azr3uVgERw3WRLbMj_BLIHveJ_A')#os.environ.get("GOOGLE_API_KEY"))

st.set_page_config(page_title="Resume Matcher AI", page_icon="📄")

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
    {resume_content if mime_type == 'text/plain' else 'Attached below'}
    
    Please provide a detailed report in Markdown:
    1. Match Score (0-100)
    2. Missing Keywords
    3. Recommended Changes to bullet points
    """
    
    parts = [prompt]
    
    # Handle different input types for Gemini
    if mime_type.startswith("image"):
        parts.append(resume_content) # Image object
    elif mime_type == "application/pdf":
        # Note: Ideally convert PDF to image for vision model or extract text
        # For simplicity here, we pass the extracted text appended to prompt
        pass 

    response = model.generate_content(parts)
    return response.text

# 3. UI Layout
st.title("📄 Resume Matcher AI")
st.markdown("Upload your resume and job description to get AI-powered feedback.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF, JPG, or PNG", type=["pdf", "jpg", "png", "txt"])

with col2:
    st.subheader("2. Job Description")
    job_desc = st.text_area("Paste job description here", height=300)

if st.button("Analyze Resume", type="primary"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing resume..."):
            try:
                # Process file
                content = None
                mime_type = uploaded_file.type
                
                if mime_type == "application/pdf":
                    content = extract_text_from_pdf(uploaded_file)
                    mime_type = "text/plain" # Treat extracted text as plain text
                elif mime_type.startswith("image"):
                    content = Image.open(uploaded_file)
                else:
                    content = uploaded_file.read().decode("utf-8")

                # Call Gemini
                result = analyze_resume(content, job_desc, mime_type)
                
                st.success("Analysis Complete!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please provide both a resume and a job description.")