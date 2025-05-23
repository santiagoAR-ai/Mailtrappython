from email.mime.text import MIMEText
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "from@example.com"
    msg["To"] = to_email

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login(MAILTRAP_USER, MAILTRAP_PASS)
        server.send_message(msg)

@app.post("/send-email/")
def send_email_endpoint(email: EmailSchema, background_tasks: BackgroundTasks):
    # Enviar el correo en segundo plano
    background_tasks.add_task(
        send_email, email.email, email.subject, email.body
    )
    return {"message": "Email enviado (verifica Mailtrap)"}
