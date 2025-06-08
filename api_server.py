from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import pdfplumber

from extract_skills import extract_skills_from_text
from generate_cover_letter import generate_cover_letter, match_skills
from docx_writer import save_cover_letter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Cover letter API is running!"}

@app.post("/generate")
async def generate(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    linkedin: str = Form(""),
    job_description: str = Form(...),
    resume_file: UploadFile = Form(...),
    role: str = Form(...),
    company: str = Form(...)
):
    try:
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        resume_path = "uploads/latest_resume.pdf"
        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())

        # Extract resume text from PDF
        with pdfplumber.open(resume_path) as pdf:
            resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # Extract skills
        resume_skills = extract_skills_from_text(resume_text, source="resume")
        jd_skills = extract_skills_from_text(job_description, source="job description")
        matched = match_skills(resume_skills, jd_skills)

        # Generate cover letter
        preview = generate_cover_letter(resume_text, job_description, matched, role, company)

        # Save to DOCX
        output_path = "outputs/latest_cover_letter.docx"
        save_cover_letter(preview, output_path, full_name, email, phone, linkedin)

        return JSONResponse({
            "message": "Cover letter generated successfully.",
            "preview": preview,
            "download_path": "/download"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download")
def download():
    file_path = "outputs/latest_cover_letter.docx"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="cover_letter.docx"
        )
    return JSONResponse(status_code=404, content={"error": "No cover letter available to download."})