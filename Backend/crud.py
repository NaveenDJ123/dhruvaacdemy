from auth import get_password_hash
from model import get_user_collection
import schemas
from bson import ObjectId

async def get_user_by_email(db, email: str):
    user_collection = get_user_collection(db)
    user = await user_collection.find_one({"email": email})
    return user

async def create_user(db, user: schemas.UserCreate):
    user_collection = get_user_collection(db)
    hashed_password = get_password_hash(user.password)
    user_dict = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    result = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user["_id"])
    created_user.pop("_id")  # Remove the MongoDB specific _id field
    return created_user
