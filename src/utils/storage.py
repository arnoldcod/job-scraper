import json
from typing import List, Dict

class JobStorage:
    def __init__(self, filename='jobs.json'):
        self.filename = filename
        self.jobs_cache = set()

    def save_jobs(self, jobs: List[Dict]):
        """Saves jobs to a JSON file, grouped by location."""
        jobs_by_location = {}
        for job in jobs:
            location = job['search_location']
            if location not in jobs_by_location:
                jobs_by_location[location] = []
            jobs_by_location[location].append(job)

        try:
            with open(self.filename, 'w') as f:
                json.dump(jobs_by_location, f, indent=2)
            print(f"Saved {len(jobs)} jobs from {len(jobs_by_location)} locations to {self.filename}")
        except Exception as e:
            print(f"Error saving jobs: {e}")

    def is_new_job(self, job: Dict) -> bool:
        """Check if a job is new (not in cache)."""
        return job['link'] not in self.jobs_cache

    def update_cache(self, jobs: List[Dict]):
        """Update the cache with new job links."""
        self.jobs_cache.update(job['link'] for job in jobs)
