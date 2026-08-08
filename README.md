# Arabic-Meeting-Video-Summarizer-
An end-to-end automated AI pipeline designed to transcribe, analyze, and summarize Arabic meetings and videos. 
The system combines state-of-the-art speech recognition, speaker identification, optical character recognition (OCR),
and large language models (LLMs) to generate structured, actionable meeting minutes and enable interactive querying.

🚀 Key Features
Advanced Arabic Transcription & Diarization: Utilizes OpenAI's Whisper model for accurate speech-to-text transcription,
integrated with Speaker Diarization and Voice Biometrics for precise speaker identification.

Visual Content Extraction (OCR): Implements an OCR system to extract, analyze, 
and summarize visual text and slides displayed on-screen during meetings or videos.

Structured LLM Summarization: Deploys and leverages state-of-the-art Large Language Models, 
including Fanar and locally-hosted Qwen models, to generate clean, structured, and actionable meeting minutes.

Interactive RAG System: Built-in Retrieval-Augmented Generation (RAG) architecture enabling users to query the meeting's
comprehensive content interactively with high precision.

Linguistic Benchmarking: Evaluates model performance using specialized linguistic metrics 
(such as BERTScore and LLM-based evaluation) tailored to capture the unique nuances of the Arabic language.

🛠 Tech Stack & Skills
Core Technologies: Natural Language Processing (NLP), Large Language Models (LLMs), Retrieval-Augmented Generation (RAG).
AI & Processing: Whisper, Speaker Diarization, Voice Biometrics, OCR, Audio Processing.
Language & Deployment: Python, Local Model Deployment (Fanar, Qwen).

📊 Project Architecture Overview
Audio/Video Ingestion & Processing: Splits audio streams, performs speaker diarization,
and transcribes spoken Arabic via Whisper.

Visual Ingestion: Captures frames and uses OCR to pull on-screen textual information.

Context Integration & LLM Processing: Feeds combined textual transcripts and visual data into local LLMs (Fanar/Qwen) for structuring.

Interactive Retrieval & Evaluation: Powers a RAG pipeline for Q&A while continuously benchmarking via metrics like BERTScore.


A local, Windows/VS Code-friendly pipeline that:

Downloads audio from a YouTube meeting recording (or uses a local file).
Preprocesses the audio (mono, 16 kHz, normalized).
Transcribes it in Arabic using Faster-Whisper (large-v3-turbo), with a simple pause-based speaker diarization.
Produces a hybrid summary: Mistral Saba 24B reads and understands the Arabic transcript, then Gemini 2.5 Flash turns that analysis into a structured Markdown/HTML report (decisions table, tasks table, key points, mind map, executive summary).
Optionally evaluates the summary with ROUGE, BERTScore, and an LLM-as-a-Judge score (Gemini).
This project was converted from a Google Colab notebook. See "Summary of all modifications made" at the end of this file for exactly what changed and why.

Project structure
Arabic_Meeting_Summarizer/
│
├── data/
│   ├── raw/            # Downloaded / input audio files land here
│   └── processed/      # Cleaned 16kHz mono WAV files land here
│
├── models/              # Reserved for any locally-cached model files
│
├── src/
│   ├── audio_downloader.py   # YouTube -> WAV download (yt-dlp)
│   ├── preprocessing.py      # Mono / resample / normalize
│   ├── transcription.py      # Faster-Whisper ASR + simple diarization
│   ├── summarizer.py         # Mistral Saba + Gemini hybrid summary
│   ├── evaluation.py         # ROUGE / BERTScore / LLM-as-a-Judge
│   ├── utils.py              # RAM/GPU monitor, memory clean-up, session id
│   └── main.py               # CLI entry point - runs the full pipeline
│
├── notebooks/
│   └── original_notebook_export.py   # The original Colab export, kept for reference only
│
├── meeting_output/       # All generated transcripts, summaries, reports
├── requirements.txt
├── README.md
├── .gitignore
└── config.py             # All settings: URL, model names, paths
What each piece is for:

File	Purpose
config.py	Single place to change the YouTube URL, model names, fast/accurate mode, and file paths. Reads API keys from environment variables / .env.
src/audio_downloader.py	Downloads the best-quality audio track of a YouTube video as WAV using yt-dlp.
src/preprocessing.py	Converts audio to mono, resamples to 16 kHz, and peak-normalizes it, ready for Whisper.
src/transcription.py	Runs Faster-Whisper for Arabic ASR and labels segments by speaker using a pause-length heuristic.
src/summarizer.py	Calls Mistral Saba to understand the Arabic transcript, then Gemini to build the final Markdown/HTML report.
src/evaluation.py	Optional: scores the summary with ROUGE, BERTScore, and Gemini-as-a-judge.
src/utils.py	Small shared helpers: RAM/GPU display, memory clean-up, session-id generation.
src/main.py	Ties everything together; run this file to execute the whole pipeline.
Removed Google Colab dependencies
Original Colab code	Why it can't run locally	Local replacement
from google.colab import userdata / userdata.get(...)	Colab Secrets only exist inside a Colab runtime.	API keys are read from environment variables via os.getenv(...), loaded from a local .env file with python-dotenv (see config.py).
!apt-get install ... libavformat-dev ...	!-prefixed shell commands only work in a notebook cell; a plain Windows machine has no apt-get at all (that's a Linux package manager).	Not needed locally: imageio-ffmpeg already ships a portable, ready-to-use FFmpeg binary for Windows/Mac/Linux, so no system package manager step is required.
!{sys.executable} -m pip install ...	Shell-magic install commands belong in requirements.txt + a one-time pip install -r requirements.txt, not scattered through the code.	All packages are listed once in requirements.txt and installed via pip install -r requirements.txt (see the setup guide below).
/content/... paths, os.chdir('/content/project')	/content is Colab's ephemeral virtual disk; it does not exist on Windows.	All paths are now relative to the project folder, computed from config.py (BASE_DIR, DATA_RAW_DIR, OUTPUT_DIR, etc.), so the project works from any drive/folder.
from IPython.display import display, HTML	IPython's rich display only renders inside a notebook (Colab/Jupyter).	summarizer.render_summary_html(...) writes a standalone .html file to meeting_output/, which you open directly in any browser.
from google.colab import files + files.upload()	Colab's manual file-upload widget doesn't exist outside Colab.	Use --audio-file <path> on the command line to point at a local audio file, or drop files directly into data/raw/.
A note on the "RAG Chatbot Integration" section
The final part of the original notebook (files.upload() of a meeting-rag-chatbot-integrated.zip, then calls like ingest_summarizer_session(...), from backend.retriever import retrieve, ask(...)) depends on an entirely separate project (a backend Python package implementing a vector store, retriever, and chat engine) that was not included in the notebook or in your upload. Because none of that code was provided, it cannot be faithfully converted — there is nothing to convert. If you have that separate RAG chatbot project, the cleanest way to combine the two is to install it as its own package (or add its folder to sys.path) and call its ingest_summarizer_session(session, output_dir) and ask(question) functions after this project finishes, pointing output_dir at this project's meeting_output/ folder.

requirements.txt
# Core ASR
faster-whisper>=1.0.0
ctranslate2>=3.25.0

# Audio download / processing
yt-dlp
imageio-ffmpeg
soundfile
torch
torchaudio

# System / utility
psutil
python-dotenv

# LLM API clients
openai>=1.0.0
google-genai>=1.64.0,<2.0.0
google-auth==2.47.0

# Report rendering
markdown2

# Evaluation (optional, only needed for --evaluate)
rouge-score
bert-score

