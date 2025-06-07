from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from generate_cover_letter import generate_cover_letter

app = FastAPI()

# Allow frontend (including Lovable) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with Lovable's actual domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (important for Render health check or basic test)
@app.get("/")
def root():
    return {"message": "Cover letter API is running!"}

# Generate cover letter endpoint
@app.post("/generate")
async def generate(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    linkedin: str = Form(""),
    job_description: str = Form(...),
    resume_file: UploadFile = Form(...)
):
    try:
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        resume_path = "uploads/latest_resume.pdf"
        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())

        output_path, preview = generate_cover_letter(
            resume_path, job_description, full_name, email, phone, linkedin
        )

        return JSONResponse({
            "message": "Cover letter generated successfully.",
            "preview": preview,
            "download_path": "/download"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Endpoint to download the latest generated cover letter
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