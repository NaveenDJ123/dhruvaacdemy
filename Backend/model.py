def get_user_collection(db):
    return db["users"]

# Define unique index on email
async def create_user_index(db):
    user_collection = get_user_collection(db)
    await user_collection.create_index("email", unique=True)
