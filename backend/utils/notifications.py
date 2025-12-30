"""
Notification manager for email and Telegram alerts
Sends notifications for new high-match jobs
"""
import asyncio
from typing import List, Dict
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Email support
try:
    import aiosmtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

# Telegram support
try:
    from telegram import Bot
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


class NotificationManager:
    """Manages notifications via email and Telegram"""
    
    def __init__(self):
        self.email_enabled = settings.email_enabled and EMAIL_AVAILABLE
        self.telegram_enabled = settings.telegram_enabled and TELEGRAM_AVAILABLE
        
        if not EMAIL_AVAILABLE and settings.email_enabled:
            logger.warning("⚠️  Email dependencies not installed")
        
        if not TELEGRAM_AVAILABLE and settings.telegram_enabled:
            logger.warning("⚠️  Telegram dependencies not installed")
    
    async def send_email(self, to_email: str, subject: str, body: str, html: bool = False):
        """
        Send email notification
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (text or HTML)
            html: Whether body is HTML
        """
        if not self.email_enabled:
            logger.debug("Email notifications disabled")
            return
        
        try:
            message = MIMEMultipart('alternative')
            message['From'] = settings.email_from
            message['To'] = to_email
            message['Subject'] = subject
            
            if html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            await aiosmtplib.send(
                message,
                hostname=settings.email_host,
                port=settings.email_port,
                username=settings.email_user,
                password=settings.email_password,
                start_tls=True
            )
            
            logger.info(f"✅ Email sent to {to_email}")
        
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
    
    async def send_telegram(self, message: str, chat_id: str = None):
        """
        Send Telegram notification
        
        Args:
            message: Message text (supports Markdown)
            chat_id: Telegram chat ID (uses default if None)
        """
        if not self.telegram_enabled:
            logger.debug("Telegram notifications disabled")
            return
        
        try:
            bot = Bot(token=settings.telegram_bot_token)
            chat_id = chat_id or settings.telegram_chat_id
            
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("✅ Telegram message sent")
        
        except Exception as e:
            logger.error(f"❌ Error sending Telegram message: {e}")
    
    async def notify_new_jobs(self, jobs: List[Dict], user_email: str = None):
        """
        Send notification about new high-match jobs
        
        Args:
            jobs: List of job dictionaries with analysis
            user_email: User email (from profile if None)
        """
        if not jobs:
            return
        
        # Filter high-match jobs (80%+)
        high_match_jobs = [j for j in jobs if j.get('match_score', 0) >= 80]
        
        if not high_match_jobs:
            logger.info("No high-match jobs to notify")
            return
        
        logger.info(f"📧 Sending notification for {len(high_match_jobs)} high-match jobs")
        
        # Email notification
        if self.email_enabled and user_email:
            subject = f"🎯 {len(high_match_jobs)} New High-Match Jobs!"
            body = self._format_email_body(high_match_jobs)
            await self.send_email(user_email, subject, body, html=True)
        
        # Telegram notification
        if self.telegram_enabled:
            message = self._format_telegram_message(high_match_jobs)
            await self.send_telegram(message)
    
    def _format_email_body(self, jobs: List[Dict]) -> str:
        """Format HTML email body for job notifications"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .job-card { 
                    border: 1px solid #ddd; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 15px 0;
                    background: #f9f9f9;
                }
                .job-title { color: #2563eb; font-size: 18px; font-weight: bold; }
                .company { color: #666; font-size: 14px; }
                .match-score { 
                    display: inline-block;
                    background: #10b981; 
                    color: white; 
                    padding: 5px 10px; 
                    border-radius: 5px;
                    font-weight: bold;
                }
                .location { color: #888; }
                .btn { 
                    display: inline-block;
                    background: #2563eb; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h2>🎯 New High-Match Jobs for You!</h2>
            <p>We found <strong>{count}</strong> new jobs matching your profile:</p>
        """.format(count=len(jobs))
        
        for job in jobs[:10]:  # Limit to 10 jobs
            html += f"""
            <div class="job-card">
                <div class="job-title">{job.get('title', 'N/A')}</div>
                <div class="company">{job.get('company', 'N/A')} • <span class="location">{job.get('location', 'N/A')}</span></div>
                <div style="margin: 10px 0;">
                    <span class="match-score">{job.get('match_score', 0):.0f}% Match</span>
                </div>
                <a href="{job.get('url', '#')}" class="btn">View Job</a>
            </div>
            """
        
        html += """
            <p><em>Check your SmartJobHunter dashboard for full details and AI recommendations!</em></p>
        </body>
        </html>
        """
        
        return html
    
    def _format_telegram_message(self, jobs: List[Dict]) -> str:
        """Format Telegram message for job notifications"""
        message = f"🎯 *{len(jobs)} New High-Match Jobs!*\n\n"
        
        for job in jobs[:5]:  # Limit to 5 jobs for Telegram
            message += f"*{job.get('title', 'N/A')}*\n"
            message += f"🏢 {job.get('company', 'N/A')}\n"
            message += f"📍 {job.get('location', 'N/A')}\n"
            message += f"✨ Match: *{job.get('match_score', 0):.0f}%*\n"
            message += f"🔗 [View Job]({job.get('url', '#')})\n\n"
        
        if len(jobs) > 5:
            message += f"_...and {len(jobs) - 5} more jobs in your dashboard!_"
        
        return message
    
    def notify_new_jobs_sync(self, jobs: List[Dict], user_email: str = None):
        """Synchronous wrapper for notify_new_jobs"""
        asyncio.run(self.notify_new_jobs(jobs, user_email))
