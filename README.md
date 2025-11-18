# adventure-content-planner

🏔️ Adventure Content Planner AI Agent

An AI-powered content strategist that turns raw activity descriptions into viral-worthy Instagram Reel & TikTok plans. Built with Python, Streamlit, and Google Gemini.

🧠 The Problem & Solution

Problem: Adventure athletes and creators spend 30-60 minutes planning, scripting, and captioning a single short-form video.
Solution: This agent uses a Large Language Model (LLM) to analyze an activity summary and generate a structured production plan in under 5 seconds, reducing the workflow by 90%.

✨ Key Features

Smart Model Selector: Automatically detects available Gemini models to prevent API 404/429 errors.

Structured Output: Forces the LLM to return data in specific Markdown tables and lists rather than unstructured text.

Rate Limit Handling: Intelligent retry logic handles API traffic jams automatically.

Exportable Plans: One-click download of the entire strategy as a text file.

🚀 Quick Start (Local Setup)

Prerequisites

You need Python 3.10+. If you are using Anaconda or an older Python version, follow step 1 carefully.

1. Create Environment

Open your terminal and run these commands to create a fresh environment:

# Create a new environment with Python 3.10
conda create -n adventure_ai python=3.10 -y

# Activate the environment
conda activate adventure_ai


2. Install Dependencies

pip install -r requirements.txt


3. Run the App

streamlit run content_planner.py


📦 Deployment (Streamlit Cloud)

This app is ready for one-click deployment:

Push this code to a public GitHub repository.

Go to share.streamlit.io.

Connect your GitHub and select this repository.

Important: In the Streamlit Cloud settings, go to Secrets and add your API key:

GEMINI_API_KEY = "your-key-here"


🏗️ Architecture

graph LR
    A[User Input] --> B(Streamlit UI)
    B --> C{Smart Model Selector}
    C -->|Selects Stable Model| D[Google Gemini API]
    D -->|System Instruction| E[Structured Content Plan]
    E --> F[Markdown/Table Display]
    E --> G[Downloadable .txt]


📄 License

MIT
