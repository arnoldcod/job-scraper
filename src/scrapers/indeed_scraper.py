import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from typing import List, Dict

class IndeedScraper(BaseScraper):
    def search_jobs(self, location: str) -> List[Dict]:
        base_url = "https://www.indeed.com/jobs"
        params = {
            "q": "junior devops",
            "l": location
        }
        
        jobs = []
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards:
                    job = {
                        'title': card.find('h2', class_='jobTitle').text.strip(),
                        'company': card.find('span', class_='companyName').text.strip(),
                        'location': card.find('div', class_='companyLocation').text.strip(),
                        'link': 'https://www.indeed.com' + card.find('a')['href'],
                        'source': 'Indeed',
                        'search_location': location
                    }
                    jobs.append(job)
        except Exception as e:
            print(f"Error scraping Indeed for {location}: {e}")
            
        return jobs