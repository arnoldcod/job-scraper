import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict

class EmailSender:
    def __init__(self, email_address: str, email_password: str):
        self.email_address = email_address
        self.email_password = email_password

    def send_job_alert(self, new_jobs: List[Dict]):
        if not self.email_address or not self.email_password:
            print("Email credentials not provided")
            return
            
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = self.email_address
        msg['Subject'] = f"New DevOps Job Listings - {datetime.now().strftime('%Y-%m-%d')}"
        
        jobs_by_location = {}
        for job in new_jobs:
            location = job['search_location']
            if location not in jobs_by_location:
                jobs_by_location[location] = []
            jobs_by_location[location].append(job)
        
        body = "New job listings found:\n\n"
        for location, jobs in jobs_by_location.items():
            body += f"=== {location} ===\n"
            body += f"Found {len(jobs)} new positions\n\n"
            
            for job in jobs:
                body += f"Title: {job['title']}\n"
                body += f"Company: {job['company']}\n"
                body += f"Location: {job['location']}\n"
                body += f"Source: {job['source']}\n"
                body += f"Link: {job['link']}\n"
                body += "-" * 50 + "\n"
            
            body += "\n"
            
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            print("Email alert sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
