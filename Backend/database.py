from motor.motor_asyncio import AsyncIOMotorClient
from model import create_user_index

MONGO_DETAILS = "mongodb+srv://naveendjgn:KM2VynpWmlAFvfuf@cluster0.fch0xlc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.my_fastapi_app

# Ensure indexes are created
async def init_db():
    await create_user_index(database)

def get_database():
    return database
