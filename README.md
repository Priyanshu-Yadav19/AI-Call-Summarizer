📞 AI Call Summariser

An AI-powered call analysis system that processes recorded audio conversations, generates structured summaries, and automatically drafts follow-up messages such as WhatsApp messages or Emails.

The system converts speech into text using Speech-to-Text (STT), analyzes the transcript using a Large Language Model (LLM), and produces actionable outputs for business communication.

This project is designed for sales calls, customer support calls, meeting recordings, and CRM workflows where quick insights and follow-up communication are required.

This repository contains two different implementations:

• main → AI4Bharat STT (local inference, higher latency)
• sarvam → Sarvam Batch API STT (low latency, production-ready)

Switch branches to explore each version.

🚀 Features

✔ Upload call recording audio

✔ Automatic Speech-to-Text transcription

✔ Clean transcript generation

✔ AI-generated call summary

✔ Draft WhatsApp follow-up message

✔ Draft Email follow-up message

✔ Modular backend architecture

✔ Environment-based configuration

✔ FastAPI API backend

✔ Simple web interface for testing

🧠 System Workflow

            User Uploads Audio
                    │
                    ▼
            Speech-to-Text Engine
                    │
                    ▼
            Transcript Generation
                    │
                    ▼
            LLM Analysis
                    │
                    ├── Call Summary
                    │
                    ├── WhatsApp Message Draft
                    │
                    └── Email Draft
🏗 Project Architecture

        ai-call-summariser
        │
        ├── app
        │   │
        │   ├── main.py                # FastAPI application entry
        │   ├── config.py              # Environment configuration
        │   ├── prompts.py             # LLM prompt templates
        │   ├── schemas.py             # API response schemas
        │   ├── utils.py               # Utility helpers
        │   ├── latency_tracker.py     # Latency monitoring
        │   │
        │   ├── stt_engine.py          # Speech-to-Text engine
        │   ├── llm_engine.py          # LLM summarization & drafting
        │   │
        │   ├── templates
        │   │   └── index.html         # Frontend upload interface
        │   │
        │   └── static
        │       └── style.css          # UI styling
        │
        ├── uploads                    # Uploaded audio files
        │
        ├── run.py                     # Application launcher
        ├── requirements.txt           # Python dependencies
        ├── .env                       # Environment variables
        ├── .env.example               # Example environment config
        ├── .gitignore
        └── README.md
⚙️ Technology Stack

       Component            | Technology            
       -------------------- | --------------------- 
       Backend API          | FastAPI               
       Programming Language | Python                
       Speech Recognition   | STT Model             
       Language Model       | LLM                   
       Frontend             | HTML / CSS            
       Configuration        | Environment Variables 


📦 Installation Guide

1️⃣ Clone the Repository
  
    git clone https://github.com/yourusername/ai-call-summariser.git
    cd ai-call-summariser
  
2️⃣ Create Virtual Environment

      python -m venv .venv

3️⃣ Activate Environment
   
    Windows
    .venv\Scripts\activate
    Linux / Mac
    source .venv/bin/activate

4️⃣ Upgrade Pip
    
    pip install --upgrade pip
5️⃣ Install Dependencies
        
    pip install -r requirements.txt
🔐 Environment Configuration

Create a .env file in the root directory.
Example:

    APP_NAME=AI Call Summariser
    APP_VERSION=1.0.0
    
    HOST=0.0.0.0
    PORT=8000
    
    UPLOAD_DIR=uploads
    
    GEMINI_API_KEY=your_api_key
    GEMINI_MODEL=gemini-3-flash-preview
    
▶️ Running the Application

Start the server:
    
    python run.py

If successful, you will see:

    Uvicorn running on http://127.0.0.1:8000
    
🌐 Access the Application
Open your browser:

    http://localhost:8000

📄 How to Use

1 Open the web interface

2 Upload an audio call recording

3 Choose output format

    > WhatsApp message   
    >Email draft

4 Click Generate

The system will return:

Transcript

Call summary

Generated follow-up message

📊 Example Output

Transcript

    Customer discussed mutual fund investment options and requested details for long-term plans.
Summary

    Customer showed interest in long-term mutual fund investment plans and requested additional information about suitable options.
WhatsApp Draft

    Hello, thank you for speaking with us today. As discussed, I will share the mutual fund investment options suitable for your long-term goals. Please let me know if you would like to proceed or need further clarification.

📁 Development Workflow

Whenever you start development:

Activate environment
   
      .venv\Scripts\activate
Run project
      
      python run.py
Stop server
    
    
    CTRL + C

    
🧩 Future Improvements

• Multilingual call support

• Audio preprocessing and noise removal

• CRM integration

• Database storage for call history

• Authentication system

• Docker containerization

• Real-time streaming transcription

• Automated follow-up scheduling

📌 Use Cases

This system can be used for:

• 📊 Sales call analysis

• 🎧 Customer support automation

• 📝 Meeting summarisation

• 🤝 CRM communication workflows

• 📁 Business call documentation

👨‍💻 Author

Priyanshu Yadav

AI / ML Engineer

India
