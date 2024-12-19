from config import Config
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.indeed_scraper import IndeedScraper
from utils.email_sender import EmailSender
from utils.storage import JobStorage
import time

class JobScraperService:
    def __init__(self):
        self.config = Config()
        self.linkedin_scraper = LinkedInScraper()
        self.indeed_scraper = IndeedScraper()
        self.email_sender = EmailSender(
            self.config.EMAIL_ADDRESS,
            self.config.EMAIL_PASSWORD
        )
        self.storage = JobStorage()

    def check_new_jobs(self):
        """Check for new job listings across all locations."""
        all_jobs = []
        
        for location in self.config.LOCATIONS:
            print(f"Searching jobs in {location}...")
            all_jobs.extend(self.linkedin_scraper.search_jobs(location))
            all_jobs.extend(self.indeed_scraper.search_jobs(location))
            time.sleep(2)  # Avoid rate limiting
        
        new_jobs = [job for job in all_jobs if self.storage.is_new_job(job)]
        
        if new_jobs:
            print(f"Found {len(new_jobs)} new jobs across {len(self.config.LOCATIONS)} locations")
            self.storage.save_jobs(new_jobs)
            self.email_sender.send_job_alert(new_jobs)
            self.storage.update_cache(new_jobs)
        else:
            print("No new jobs found")

def main():
    service = JobScraperService()
    
    # Run initial check
    service.check_new_jobs()
    
    # Schedule periodic checks
    while True:
        time.sleep(Config.CHECK_INTERVAL)
        service.check_new_jobs()

if __name__ == "__main__":
    main()