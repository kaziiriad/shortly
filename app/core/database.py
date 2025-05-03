import motor.motor_asyncio
from .config import settings
from functools import wraps

def with_collection(method):
    """Decorator to provide the collection to the method."""
    @wraps(method)
    async def wrapper(self, collection_name, *args, **kwargs):
        collection = self.db.get_collection(collection_name)
        return await method(self, collection, *args, **kwargs)
    return wrapper

class MongoDB:
    def __init__(self, db_url: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

    async def close(self):
        self.client.close()

    @with_collection
    async def get_all_items(self, collection, **kwargs):
        items = await collection.find().to_list(length=None)
        return items
    
    @with_collection
    async def get_item_by_id(self, collection, item_id: str, **kwargs):
        item = await collection.find_one({"_id": item_id})
        return item
    
    @with_collection
    async def create_item(self, collection, item_data: dict, **kwargs):
        result = await collection.insert_one(item_data)
        new_item = await collection.find_one({"_id": result.inserted_id})
        return new_item
    
    @with_collection
    async def update_item(self, collection, item_id: str, item_data: dict, **kwargs):
        if await collection.find_one({"_id": item_id}) is None:
            return False
        
        await collection.update_one({"_id": item_id}, {"$set": item_data})
        return True
    
    @with_collection
    async def delete_item(self, collection, item_id: str, **kwargs):
        if await collection.find_one({"_id": item_id}) is None:
            return False
        await collection.delete_one({"_id": item_id})
        return True
    
db = MongoDB(settings.DB_URL, settings.DB_NAME)
