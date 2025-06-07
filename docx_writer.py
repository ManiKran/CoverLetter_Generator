# docx_writer.py

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def save_cover_letter_to_docx(text: str, role: str, company: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(
        output_dir,
        f"cover_letter_{role.replace(' ', '_')}_{company.replace(' ', '_')}.docx"
    )

    doc = Document()
    lines = text.strip().splitlines()
    
    # Extract name and contact info
    name = lines[0].strip() if lines else "Full Name"
    contact = lines[1].strip() if len(lines) > 1 else "email@example.com | (123) 456-7890 | linkedin.com/in/example"

    # Name formatting
    name_para = doc.add_paragraph()
    name_run = name_para.add_run(name)
    name_run.font.name = "Times New Roman"
    name_run.font.size = Pt(14)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Contact formatting
    contact_para = doc.add_paragraph()
    contact_run = contact_para.add_run(contact)
    contact_run.font.name = "Times New Roman"
    contact_run.font.size = Pt(12)
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()  # Spacer

    # Body formatting
    for line in lines[2:]:
        if line.strip() == "":
            doc.add_paragraph()
        else:
            para = doc.add_paragraph()
            run = para.add_run(line.strip())
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

    doc.save(file_path)
    print(f"✅ Cover letter saved to: {file_path}")