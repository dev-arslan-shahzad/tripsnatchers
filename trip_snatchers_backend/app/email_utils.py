import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import secrets

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")  # Default to 8080 if not set

def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Generic function to send emails
    """
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_verification_email(user_email: str, token: str) -> bool:
    """
    Send email verification link to user
    """
    verification_link = f"{FRONTEND_URL}/verify-email?token={token}"
    print(f"Sending verification email to {user_email} with link: {verification_link}")  # Debug log
    
    subject = "Verify Your Trip Snatchers Account"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">Welcome to Trip Snatchers! ✈️</h2>
            <p>Thank you for registering. Please verify your email address to start tracking holiday deals.</p>
            <p>Click the button below to verify your email:</p>
            <p style="text-align: center;">
                <a href="{verification_link}" 
                   style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
                    Verify Email
                </a>
            </p>
            <p>Or copy and paste this link in your browser:</p>
            <p style="background-color: #f5f5f5; padding: 10px; border-radius: 4px; word-break: break-all;">
                {verification_link}
            </p>
            <p><strong>Note:</strong> This link will expire in 24 hours.</p>
            <p style="color: #666; font-size: 0.9em;">If you didn't create an account with Trip Snatchers, please ignore this email.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        print(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")  # Debug log
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("SMTP login successful")  # Debug log
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")  # Debug log
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")  # Error log
        return False

def send_price_alert(user_email: str, holiday_url: str, target_price: float) -> bool:
    """
    Send an email alert when a holiday price matches or goes below target price
    """
    subject = "Your Trip Snatchers Alert!"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">Great news! 🎉</h2>
            <p>Your tracked holiday has reached your target price of €{target_price}!</p>
            <p style="text-align: center;">
                <a href="{holiday_url}" 
                   style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
                    View Holiday Deal
                </a>
            </p>
            <p><strong>Don't wait too long</strong> - prices can change quickly!</p>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send price alert: {str(e)}")
        return False

def generate_verification_token() -> tuple[str, datetime]:
    """
    Generate a verification token and its expiry timestamp
    """
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=24)
    return token, expires 