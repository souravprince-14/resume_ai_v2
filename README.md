# Resume Matcher AI

A simple Streamlit app that analyzes an uploaded resume against a pasted job description using Google Generative AI (Gemini). The app performs two main tasks:

1. Strictly classifies whether an uploaded document looks like a resume.
2. If it is a resume, produces a detailed Markdown report comparing the resume to the job description (match score, missing keywords, and recommended bullet edits).

This README reflects the behavior implemented in app.py.

## Features
- Resume/TXT upload (PDF or plain text)
- Strict resume detection using Gemini
- Resume vs. Job Description analysis with a career-coach style report
- Outputs a Markdown report including:
  - Match Score (0–100)
  - Missing Keywords
  - Recommended changes to bullet points
- Simple Streamlit UI with upload, job description text area, and an analyze button
- Basic error handling and in-app warnings

## Prerequisites
- Python 3.10+ (3.11/3.12 recommended)
- A Google Generative AI (Gemini) API key
- Internet access for the Gemini API
- A virtual environment is recommended

## Required Python packages
The app uses:
- streamlit
- google-generativeai
- python-dotenv
- PyPDF2

You can install dependencies via:
```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt, install directly:
```bash
pip install streamlit google-generativeai python-dotenv PyPDF2
```

## Environment variables
The app expects an environment variable named `GENAI_API_KEY`. You can provide it in one of two ways:

1. Create a `.env` file in the project root (this repository includes `.gitignore` to avoid committing secrets):

```
GENAI_API_KEY=your_google_genai_api_key_here
```

2. Or set the environment variable in your OS / hosting environment.

Example (macOS / Linux):
```bash
export GENAI_API_KEY="your_google_genai_api_key_here"
```

Example (PowerShell):
```powershell
setx GENAI_API_KEY "your_google_genai_api_key_here"
```

When the app starts, it will warn in the UI if `GENAI_API_KEY` is not set.

## Supported resume file types
- PDF (`application/pdf`) — parsed with PyPDF2
- Plain text (`text/plain`)

If you upload other file types, the app will show an error.

## How it works (high level)
- The uploaded document's text is extracted (PDF or TXT).
- The app calls Gemini (`gemini-2.5-flash`) as a strict classifier to decide whether the text is a resume. The classifier expects an exact reply of `RESUME` or `NOT_RESUME`.
- If classified as a resume, the app sends the resume content and the pasted job description to Gemini to generate a Markdown report:
  - Match Score (0–100)
  - Missing keywords
  - Recommended improvements to bullet points
- The resulting report is displayed directly in the Streamlit UI.

Important: app.py currently uses the model name `gemini-2.5-flash` when creating a GenerativeModel instance. Ensure your Google GenAI access supports that model or update the model name accordingly.

## Running the app locally
1. Create and activate a virtual environment:
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set `GENAI_API_KEY` (see Environment variables section).

4. Run Streamlit:
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## UI usage
1. In the "Upload Resume" panel, upload a PDF or TXT resume.
2. In the "Job Description" panel, paste the job description text.
3. Click "Analyze Resume".
4. The app will validate file type, check if the document looks like a resume, then produce the analysis report in Markdown.

If either the resume or job description is missing, the app warns and does not proceed.

## Troubleshooting
- "GENAI_API_KEY is not set" warning: make sure the environment variable or `.env` is set correctly.
- PDF extraction problems: some PDFs (scanned images) won't yield text — convert to text-first PDFs or use OCR before uploading.
- Model/permission errors: ensure your Google GenAI access supports the chosen model (`gemini-2.5-flash`) and your key has the right permissions.
- Large documents: the app truncates content when building prompts (the classifier uses the first part of the document). For very long resumes or JDs, consider pasting the most relevant sections.

## Security — handling API keys
- Treat any committed API key as compromised. Rotate the key immediately if accidentally committed.
- Keep keys out of source control (use `.env` and `.gitignore`, or store secrets in your cloud/hosting provider).
- If a key was committed historically, consider removing it from git history using BFG or git filter-repo (rewriting history is disruptive; coordinate with collaborators).

## Deployment notes
- Streamlit Cloud / Render / Fly.io: set the `GENAI_API_KEY` via the dashboard secrets environment variables.
- This app depends on an external Gemini API — it must be able to reach Google GenAI from the deployment environment.

## Extending the app
- Add a small pre-flight integration test to validate `GENAI_API_KEY` and that the configured model is reachable.
- Add support for richer resume parsing (structured sections, experience dates) and more granular scoring.
- Limit prompt length or chunk large documents to avoid prompt-size issues.

---

If you'd like, I can:
- Push this README to the repository as a replacement,
- Generate or validate a requirements.txt,
- Or add a small health-check endpoint and CI job to validate the GENAI connectivity before launching.
