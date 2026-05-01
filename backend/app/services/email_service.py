import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import aiosmtplib
from email.message import EmailMessage

from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD

    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        content_type: str = "html",
        from_email: Optional[str] = None
    ) -> bool:
        """Send email asynchronously"""
        try:
            # Create message
            msg = EmailMessage()
            msg["From"] = from_email or self.smtp_username or "noreply@aisocialintel.com"
            msg["To"] = to_email
            msg["Subject"] = subject

            # Set content type
            if content_type == "html":
                msg.set_content(content, subtype="html")
            else:
                msg.set_content(content)

            # Send email
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=True
            )

            return True

        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_email_sync(
        self,
        to_email: str,
        subject: str,
        content: str,
        content_type: str = "html",
        from_email: Optional[str] = None
    ) -> bool:
        """Send email synchronously (fallback method)"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = from_email or self.smtp_username or "noreply@aisocialintel.com"
            msg["To"] = to_email
            msg["Subject"] = subject

            # Attach content
            if content_type == "html":
                body = MIMEText(content, "html")
            else:
                body = MIMEText(content, "plain")

            msg.attach(body)

            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)

            # Send email
            server.send_message(msg)
            server.quit()

            return True

        except Exception as e:
            print(f"Synchronous email sending failed: {e}")
            return False

    async def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to AI Social Intelligence!"

        html_content = f"""
        <html>
        <body>
            <h2>Welcome to AI Social Intelligence, {user_name}!</h2>
            <p>Thank you for joining our platform. Here's what you can do:</p>
            <ul>
                <li>Monitor social media conversations in real-time</li>
                <li>Get AI-powered sentiment analysis</li>
                <li>Receive automated business reports</li>
                <li>Track hiring trends and tech insights</li>
            </ul>
            <p>Get started by connecting your social media accounts and exploring your dashboard.</p>
            <br>
            <p>Best regards,<br>The AI Social Intelligence Team</p>
        </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_content)

    async def send_report_email(
        self,
        to_email: str,
        report_title: str,
        report_content: str,
        report_type: str = "daily"
    ) -> bool:
        """Send automated report email"""
        subject = f"AI Social Intelligence - {report_title} ({report_type.title()} Report)"

        html_content = f"""
        <html>
        <body>
            <h2>{report_title}</h2>
            <p>Your automated {report_type} business intelligence report is ready.</p>

            <div style="border: 1px solid #ddd; padding: 20px; margin: 20px 0;">
                {report_content}
            </div>

            <p>Login to your dashboard for detailed analytics and interactive visualizations.</p>

            <br>
            <p>Best regards,<br>AI Social Intelligence System</p>
            <hr>
            <small>This is an automated report. Please do not reply to this email.</small>
        </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_content)

    async def send_alert_email(
        self,
        to_email: str,
        alert_type: str,
        alert_message: str,
        severity: str = "medium"
    ) -> bool:
        """Send alert notifications"""
        subject = f"AI Social Intelligence Alert - {alert_type}"

        severity_colors = {
            "low": "#28a745",
            "medium": "#ffc107",
            "high": "#dc3545"
        }

        html_content = f"""
        <html>
        <body>
            <h2 style="color: {severity_colors.get(severity, '#ffc107')};">Alert: {alert_type}</h2>
            <p>{alert_message}</p>

            <p>Please check your dashboard for more details.</p>

            <br>
            <p>AI Social Intelligence Monitoring System</p>
        </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_content)