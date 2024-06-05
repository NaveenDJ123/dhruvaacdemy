from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError
import model, schemas, crud
from auth import verify_password
from database import get_database
from aiocache import caches

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        },
        'plugins': []
    }
})

@app.on_event("startup")
async def on_startup():
    await clear_cache()

async def clear_cache():
    cache = caches.get('default')
    await cache.clear()
    print("Cache cleared")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/signup/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db=Depends(get_database)):
    try:
        created_user = await crud.create_user(db, user)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created_user

@app.post("/login/")
async def login(data: schemas.UserLogin, db=Depends(get_database)):
    user = await crud.get_user_by_email(db, email=data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}
