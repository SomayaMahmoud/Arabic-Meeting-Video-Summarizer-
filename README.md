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
