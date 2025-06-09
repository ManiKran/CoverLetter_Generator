# 📝 AI-Powered Cover Letter Generator

Generate personalized, professional cover letters in seconds — just upload your resume, paste a job description, and let the AI do the rest.

Built and deployed in under a day using modern tools like FastAPI, OpenAI's GPT-4o, and React (Lovable UI).

---

## 🚀 Features

- ✅ Upload your **resume (PDF)**
- ✅ Paste any **job description**
- ✅ Fill in your **name, contact, role, and company**
- ✅ Instantly generate a **ready-to-submit, AI-crafted cover letter**
- ✅ Download as a clean, properly formatted `.docx` file

---

## 🧠 Powered By

- **GPT-4o** for intelligent skill extraction and letter generation  
- **FastAPI** backend for clean API endpoints  
- **python-docx** for rich Word document creation  
- **pdfplumber** for accurate PDF resume parsing  
- **React + Tailwind (Lovable)** for smooth UX  

---

## 🛠️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/cover-letter-ai.git
   cd cover-letter-ai

2. **Set up environment variables:**
   Create a .env file in the root with your OpenAI key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Run the backend:**
   ```bash
   uvicorn api_server:app --host 0.0.0.0 --port 10000

✅ Live Demo

🔗 https://coverlettergenerator.lovable.app/
🕒 Note: It might not be live.(mail to: manikiran.chatrathi@outlook.com to try it out)
