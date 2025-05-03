from datetime import datetime
import random
import logging
from ..core.database import db
from ..models.schemas import URLSchema
from ..core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class URLService:
    def __init__(self):
        self.db = db
        self.collection_name = "urls"
    
    async def generate_short_url_id(self):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        short_url_id = "".join(random.choice(characters) for _ in range(6))
        return short_url_id
    
    async def create_short_url(self, original_url: str):
        short_url_id = await self.generate_short_url_id()
        short_url = f"{settings.BASE_URL}/urls/{short_url_id}"
        
        url_data = {
            "_id": short_url_id,  # Use the short_url_id as the document _id
            "short_url": short_url,
            "original_url": original_url,
            "created_at": str(datetime.now()),
            "visits": 0
        }
        
        logger.debug(f"Creating URL with data: {url_data}")
        new_url = await self.db.create_item(self.collection_name, url_data)
        logger.debug(f"Created URL: {new_url}")
        return URLSchema(**new_url)
    
    async def get_original_url(self, short_url_id: str):
        logger.debug(f"Looking up URL with short_url_id: {short_url_id}")
        url = await self.db.get_item_by_id(self.collection_name, short_url_id)
        logger.debug(f"Found URL: {url}")
        if url:
            # Increment the visit count
            await self.db.update_item(
                self.collection_name, 
                short_url_id, 
                {"visits": url.get("visits", 0) + 1}
            )
            return URLSchema(**url)
        return None

