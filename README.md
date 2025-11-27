# Resume Matcher AI

This Streamlit app analyzes an uploaded resume against a pasted job description using a local Ollama model (preferred) or the Ollama CLI as a fallback. Optionally, if you have LangChain + Ollama integrations installed, the app will use `OllamaLLM` via LangChain.

## Prerequisites
- Python 3.10+ (3.11/3.12 recommended)
- Ollama installed and daemon running. Ensure the model you want is available locally, e.g. `ollama:latest`.
- A virtual environment (recommended)

## Setup
1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Confirm Ollama is running and the model exists:

```powershell
ollama ls
```

If the daemon is not running, start it according to your Ollama installation instructions.

## Run the app

```powershell
streamlit run app.py
```

## Notes
- The app tries to use `langchain_core` + `langchain_ollama` if installed. If those packages aren't available or the LangChain call fails, it falls back to the `ollama` CLI (`ollama generate` or `ollama run`).
- Use the `Model name` input in the UI to choose a model (default: `ollama:latest`).
- Enable `Show debug logs` to display error details returned from the Ollama CLI or LangChain runtime.

If you want, I can pin specific versions for `langchain-core` and `langchain-ollama` that I've tested, or add a small integration test harness to validate Ollama connectivity automatically.

## Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Push your repository to GitHub: ✅ **Done** → https://github.com/souravprince-14/resume_ai
2. Go to https://share.streamlit.io and sign in with your GitHub account.
3. Click **"New app"**, select your repository (`resume_ai`), branch (`main`), and main file (`app.py`).
4. Streamlit Cloud will automatically install `requirements.txt` and run your app.
5. Your app will be live at `https://share.streamlit.io/souravprince-14/resume_ai`.

**Note:** Streamlit Cloud runs on public servers. If Ollama is running on your local machine, the app won't be able to reach it remotely. To use Ollama on Streamlit Cloud, you'll need to either:
- Run Ollama on a remote server accessible via HTTP (e.g., `http://your-server:11434`).
- Use a cloud-hosted LLM API (e.g., OpenAI, Anthropic) instead of local Ollama.

### Option 2: Render or Fly.io (For remote Ollama or cloud LLM)
1. Create an account on https://render.com or https://fly.io.
2. Connect your GitHub repository.
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `streamlit run app.py --server.port $PORT --server.headless true`
5. Deploy and configure environment variables if using a cloud LLM.

### Option 3: Keep running locally
- Run `streamlit run app.py` on your machine and access it at `http://localhost:8501`.
- This is ideal if Ollama is running on your local system.