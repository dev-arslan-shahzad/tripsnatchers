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
    Generic function to send emails with improved deliverability
    """
    msg = MIMEMultipart('alternative')
    
    # Format From header with display name for better deliverability
    from_name = "Trip Snatchers"
    msg['From'] = f"{from_name} <{FROM_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add headers to improve deliverability
    msg['Message-ID'] = f"<{secrets.token_hex(16)}@tripsnatchers.com>"
    msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    msg['List-Unsubscribe'] = f"<mailto:{FROM_EMAIL}?subject=unsubscribe>"
    msg['Precedence'] = 'bulk'
    msg['X-Mailer'] = 'Trip Snatchers Mailer 1.0'
    
    # Add plain text version first (important for spam filters)
    plain_text = body.replace('<br>', '\n').replace('<p>', '\n').replace('</p>', '\n')
    plain_text = ' '.join(plain_text.split())  # Normalize whitespace
    msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    
    # Add HTML version
    msg.attach(MIMEText(body, 'html', 'utf-8'))

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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #2D8A67; margin: 0;">Welcome to Trip Snatchers! ✈️</h2>
            </div>
            <p style="margin: 16px 0;">Hi there,</p>
            <p style="margin: 16px 0;">Thank you for registering with Trip Snatchers. To ensure the security of your account and start tracking amazing holiday deals, please verify your email address.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_link}" 
                   style="background-color: #2D8A67; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
                    Verify Email
                </a>
            </div>
            <p style="margin: 16px 0;">If the button doesn't work, you can copy and paste this link into your browser:</p>
            <p style="background-color: #f5f5f5; padding: 10px; border-radius: 4px; word-break: break-all; margin: 16px 0;">
                {verification_link}
            </p>
            <p style="margin: 16px 0;"><strong>Note:</strong> This link will expire in 24 hours for security reasons.</p>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 0.9em; margin: 8px 0;">If you didn't create an account with Trip Snatchers, please ignore this email.</p>
                <p style="color: #666; font-size: 0.9em; margin: 8px 0;">
                    © 2025 Trip Snatchers. All rights reserved.<br>
                    You received this email because you signed up for Trip Snatchers.
                </p>
                <p style="color: #666; font-size: 0.9em; margin: 8px 0;">
                    To unsubscribe from these emails, <a href="mailto:{FROM_EMAIL}?subject=unsubscribe" style="color: #2D8A67;">click here</a>
                </p>
            </div>
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
            <h2 style="color: #2D8A67;">Great news! 🎉</h2>
            <p>Your tracked holiday has reached your target price of €{target_price}!</p>
            <p style="text-align: center;">
                <a href="{holiday_url}" 
                   style="background-color: #2D8A67; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
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