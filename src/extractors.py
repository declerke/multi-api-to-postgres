import requests
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class BaseExtractor:
    def _get(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from {url}: {e}")
            return None

class AdviceExtractor(BaseExtractor):
    def fetch_advice(self):
        data = self._get(Config.ADVICE_API_URL)
        return data.get("slip") if data else None

class QuoteExtractor(BaseExtractor):
    def fetch_quote(self):
        return self._get(Config.QUOTABLE_API_URL)

class DogExtractor(BaseExtractor):
    def fetch_dog_image(self):
        data = self._get(Config.DOG_API_URL)
        if data and data.get("status") == "success":
            return {"image_url": data.get("message")}
        return None