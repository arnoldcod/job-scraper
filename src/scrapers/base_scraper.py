from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    @abstractmethod
    def search_jobs(self, location: str) -> List[Dict]:
        """Search jobs for a given location"""
        pass