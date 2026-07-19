from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(path, data):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Data Audit Report", styles["Title"]))
    content.append(Spacer(1, 10))

    for key, value in data.items():
        content.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
        content.append(Spacer(1, 8))

    doc.build(content)