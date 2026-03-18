📞 AI Call Summariser Agent

An AI-powered call analysis system that converts audio conversations into structured insights and automatically generates customer-ready follow-up communication (WhatsApp / Email).

This repository contains two different implementations:

• main → AI4Bharat STT (local inference, higher latency)
• sarvam → Sarvam Batch API STT (low latency, production-ready)

Switch branches to explore each version.

The system supports dual Speech-to-Text (STT) backends:

⚡ AI4Bharat (Local Inference) — Fast, offline, experimental

☁️ Sarvam AI (Batch API) — Scalable, production-ready

🚀 Overview

This system processes call recordings through a complete AI pipeline:

🎙 Convert speech → text (STT)

🧠 Analyze transcript using LLM

✉️ Generate actionable outputs

✔ Call Summary
✔ WhatsApp Follow-up
✔ Email Draft

✨ Features

📤 Upload call recordings

🔄 Dual STT backend support (AI4Bharat / Sarvam)

📝 Clean transcript generation

🧠 AI-powered call summarization

💬 WhatsApp draft generation

📧 Email draft generation

⏱ Latency tracking (STT + LLM)

⚙️ Environment-based configuration

⚡ FastAPI backend (production-ready)

🎨 Clean UI for testing & demo

🧠 System Workflow
            
            User Uploads Audio
                    │
                    ▼
               STT Engine (Selectable)
               ├── AI4Bharat (Local)
               └── Sarvam (Batch API)
                    │
                    ▼
               Transcript Generation
                    │
                    ▼
               LLM Processing (Gemini)
                    │
                    ├── Call Summary
                    ├── WhatsApp Draft
                    └── Email Draft
        
🌿 Branch Strategy

Branch	Description

main	AI4Bharat STT (Local inference, no API needed)

sarvam	Sarvam Batch STT (Production, long audio support)

⚙️ Tech Stack

            | Component  | Technology         |
            | ---------- | ------------------ |
            | Backend    | FastAPI            |
            | Language   | Python             |
            | STT Models | AI4Bharat / Sarvam |
            | LLM        | Gemini             |
            | Frontend   | HTML + CSS         |
            | Config     | dotenv             |



📦 Installation
1️⃣ Clone Repository

            git clone https://github.com/yourusername/ai-call-summariser.git
            cd ai-call-summariser
2️⃣ Select Branch

👉 AI4Bharat (Local STT)

            git checkout main

👉 Sarvam (Cloud STT)

            git checkout sarvam
            
3️⃣ Create Virtual Environment

            python -m venv .venv
4️⃣ Activate Environment

Windows

            .venv\Scripts\activate

Mac/Linux

            source .venv/bin/activate
5️⃣ Install Dependencies
            
            pip install -r requirements.txt
🔐 Environment Setup

Create .env file:

            APP_NAME=AI Call Summariser
            APP_VERSION=1.0.0
            
            HOST=0.0.0.0
            PORT=8000
            
            UPLOAD_DIR=uploads
            TRANSCRIPT_DIR=transcripts
            
            GEMINI_API_KEY=your_api_key
            GEMINI_MODEL=gemini-3-flash-preview

🔹 Sarvam Branch 
            
            SARVAM_API_KEY=your_sarvam_api_key
            SARVAM_MODEL=saaras:v3

▶️ Run the App

            python run.py
            
🌐 Access UI

            http://localhost:8000
            
📄 How It Works

1 Upload audio file

2 Select output type

    WhatsApp
      |
    Email

Click Generate Output

📊 Sample Output

📝 Transcript

            Customer discussed mutual fund investment options...

📌 Summary
            
            Customer showed interest in long-term investment plans...

💬 WhatsApp Draft

            Hello, thank you for speaking with us today...

⚡ Performance Insights
           
            | Metric         | Value    |
            | -------------- | -------- |
            | STT Latency    | ~15s–60s |
            | LLM Summary    | ~8s      |
            | Email Draft    | ~25s     |
            | WhatsApp Draft | ~7s      |

🔍 Branch Comparison

            | Feature          | AI4Bharat | Sarvam    |
            | ---------------- | --------- | --------- |
            | Mode             | Local     | Cloud     |
            | Setup            | Complex   | Easy      |
            | Speed            | Fast      | Medium    |
            | Audio Length     | Limited   | Unlimited |
            | Production Ready | Medium    | High      |


📁 Project Structure
            
            ai-call-summariser
            │
            ├── app
            │   ├── main.py
            │   ├── config.py
            │   ├── prompts.py
            │   ├── schemas.py
            │   ├── utils.py
            │   ├── latency_tracker.py
            │   ├── stt_engine.py
            │   ├── llm_engine.py
            │   │
            │   ├── templates
            │   └── static
            │
            ├── uploads
            ├── transcripts
            ├── run.py
            ├── requirements.txt
            ├── .env
            └── README.md
            
🔄 Development Workflow

            .venv\Scripts\activate
            python run.py
              CTRL + C
🧩 Future Enhancements

  🌍 Multilingual support

  🎧 Audio noise cleaning

 ⚡ Real-time streaming STT

 🗄 Database integration

 🔐 Authentication

🐳 Docker deployment

📅 Auto follow-up scheduling

📌 Use Cases

   📊 Sales call analysis
            
   🎧 Customer support automation
            
   📝 Meeting summarisation
   
   🤝 CRM workflows
             
   📁 Call documentation

👨‍💻 Author

Priyanshu Yadav
AI / ML Engineer
India 🇮🇳

🧠 Resume Highlight

Built a production-ready AI call analysis system with dual STT backends (AI4Bharat & Sarvam), enabling scalable transcription, summarization, and automated communication workflows.
