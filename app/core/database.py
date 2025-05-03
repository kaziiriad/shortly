import motor.motor_asyncio
import logging
from .config import settings
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def with_collection(method):
    """Decorator to provide the collection to the method."""
    @wraps(method)
    async def wrapper(self, collection_name, *args, **kwargs):
        collection = self.db.get_collection(collection_name)
        return await method(self, collection, *args, **kwargs)
    return wrapper

class MongoDB:
    def __init__(self, db_url: str, db_name: str):
        logger.debug(f"Initializing MongoDB connection to {db_url}, database: {db_name}")
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
            self.db = self.client[db_name]
            logger.debug("MongoDB connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB connection: {str(e)}")
            raise

    async def close(self):
        try:
            logger.debug("Closing MongoDB connection")
            self.client.close()
            logger.debug("MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")
            raise

    @with_collection
    async def get_all_items(self, collection, **kwargs):
        try:
            logger.debug(f"Getting all items from collection")
            items = await collection.find().to_list(length=None)
            return items
        except Exception as e:
            logger.error(f"Error getting all items: {str(e)}")
            raise
    
    @with_collection
    async def get_item_by_id(self, collection, item_id: str, **kwargs):
        try:
            logger.debug(f"Getting item by ID: {item_id}")
            item = await collection.find_one({"_id": item_id})
            return item
        except Exception as e:
            logger.error(f"Error getting item by ID: {str(e)}")
            raise
    
    @with_collection
    async def create_item(self, collection, item_data: dict, **kwargs):
        try:
            logger.debug(f"Creating item: {item_data}")
            result = await collection.insert_one(item_data)
            logger.debug(f"Insert result: {result.inserted_id}")
            new_item = await collection.find_one({"_id": result.inserted_id})
            return new_item
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            raise
    
    @with_collection
    async def update_item(self, collection, item_id: str, item_data: dict, **kwargs):
        try:
            logger.debug(f"Updating item with ID: {item_id}, data: {item_data}")
            if await collection.find_one({"_id": item_id}) is None:
                logger.warning(f"Item with ID {item_id} not found for update")
                return False
            
            result = await collection.update_one({"_id": item_id}, {"$set": item_data})
            logger.debug(f"Update result: matched={result.matched_count}, modified={result.modified_count}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            raise
    
    @with_collection
    async def delete_item(self, collection, item_id: str, **kwargs):
        try:
            logger.debug(f"Deleting item with ID: {item_id}")
            if await collection.find_one({"_id": item_id}) is None:
                logger.warning(f"Item with ID {item_id} not found for deletion")
                return False
            
            result = await collection.delete_one({"_id": item_id})
            logger.debug(f"Delete result: deleted={result.deleted_count}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting item: {str(e)}")
            raise
    
db = MongoDB(settings.DB_URL, settings.DB_NAME)
