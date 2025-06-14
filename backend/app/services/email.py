import emails
from emails.template import JinjaTemplate
from typing import Any
from backend.app.core.config import settings
from backend.app.models.models import Appointment
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: dict[str, Any] = {},
) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    return response

def send_appointment_confirmation(appointment: Appointment) -> None:
    subject = f"Appointment Confirmation: {appointment.title}"
    html_content = f"""
    <h1>Appointment Confirmation</h1>
    <p>Dear {appointment.user.full_name},</p>
    <p>Your appointment has been scheduled:</p>
    <ul>
        <li>Title: {appointment.title}</li>
        <li>Date: {appointment.start_time.strftime('%Y-%m-%d')}</li>
        <li>Time: {appointment.start_time.strftime('%H:%M')} - {appointment.end_time.strftime('%H:%M')}</li>
        <li>Status: {appointment.status}</li>
    </ul>
    <p>Description: {appointment.description}</p>
    <p>Thank you for using our booking system!</p>
    """
    send_email(
        email_to=appointment.user.email,
        subject_template=subject,
        html_template=html_content,
        environment={"appointment": appointment}
    )

def send_appointment_reminder(appointment: Appointment) -> None:
    subject = f"Appointment Reminder: {appointment.title}"
    html_content = f"""
    <h1>Appointment Reminder</h1>
    <p>Dear {appointment.user.full_name},</p>
    <p>This is a reminder for your upcoming appointment:</p>
    <ul>
        <li>Title: {appointment.title}</li>
        <li>Date: {appointment.start_time.strftime('%Y-%m-%d')}</li>
        <li>Time: {appointment.start_time.strftime('%H:%M')} - {appointment.end_time.strftime('%H:%M')}</li>
    </ul>
    <p>Description: {appointment.description}</p>
    <p>We look forward to seeing you!</p>
    """
    send_email(
        email_to=appointment.user.email,
        subject_template=subject,
        html_template=html_content,
        environment={"appointment": appointment}
    )

def send_appointment_confirmation(email: str, appointment_details: dict):
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = email
    msg['Subject'] = "Appointment Confirmation"

    body = f"""
    Your appointment has been confirmed:
    Date: {appointment_details['date']}
    Time: {appointment_details['time']}
    Service: {appointment_details['service']}
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}") 