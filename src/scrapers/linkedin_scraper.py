import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from typing import List, Dict
import time

class LinkedInScraper(BaseScraper):
    def search_jobs(self, location: str) -> List[Dict]:
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        params = {
            "keywords": "junior devops",
            "location": location,
            "start": 0
        }
        
        jobs = []
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job-search-card')
                
                for card in job_cards:
                    job = {
                        'title': card.find('h3', class_='base-search-card__title').text.strip(),
                        'company': card.find('h4', class_='base-search-card__subtitle').text.strip(),
                        'location': card.find('span', class_='job-search-card__location').text.strip(),
                        'link': card.find('a', class_='base-card__full-link')['href'],
                        'source': 'LinkedIn',
                        'search_location': location
                    }
                    jobs.append(job)
        except Exception as e:
            print(f"Error scraping LinkedIn for {location}: {e}")
        
        return jobs