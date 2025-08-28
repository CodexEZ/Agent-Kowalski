from fastapi import FastAPI, Response, Request
from models.gemini_chat_model import GeminiChatModel, Chat
from models.api_models import ResponseSchema, Status
from models.api_models import UserSchema
import asyncio
import uvicorn
import sys
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from utils.gemini_call import gemini
from db.crud import UserManager
from loguru import logger
from pymongo.errors import DuplicateKeyError

load_dotenv()
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sessions = {}

# Initialize MCP client once (on startup)
mcp_client = None


@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        logger.info("Synchronizing sessions")
        sessions = await UserManager.getSessions()
        logger.info("Sessions Synchronized")
    except Exception as e:
        logger.info(f"Synchronizng Failed\nstacktrace:{e}")
    
    yield
    print("Shutting Down")


api = FastAPI(lifespan=lifespan)
api.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)
@api.post("/register")
async def register(user_data:UserSchema):
    try:
        response:ResponseSchema= await UserManager.create_user(user_data)
        if response.status == Status.SUCCESS:
            logger.info(f"User {user_data.username} registered successfully.")
        else:
            logger.warning(f"User registration failed for {user_data.username}: {response.content}")
        return response.model_dump()
    except DuplicateKeyError:
        logger.warning(f"Registration failed: Username {user_data.username} already exists.")
        return ResponseSchema(status=Status.ERROR, content="Username already registered").model_dump()
    except Exception as e:
        logger.error(f"Error during registration for {user_data.username}: {e}")
        return ResponseSchema(status=Status.ERROR, content="An unexpected error occurred during registration").model_dump()
        
@api.post("/login")
async def login(user_data:UserSchema):
    try:
        response:ResponseSchema = await UserManager.login(user_data, sessions)
        if response.status == Status.SUCCESS:
            logger.info(f"User {user_data.username} logged in successfully.")
        else:
            logger.warning(f"Login failed for {user_data.username}: {response.content}")
        return response.model_dump()
    except Exception as e:
        logger.error(f"Error during login for {user_data.username}: {e}")
        return ResponseSchema(status=Status.ERROR, content="An unexpected error occurred during login").model_dump()

@api.post("/logout")
async def logout(request:Request):
    session_id = request.headers.get("Authorization")
    response:ResponseSchema = await UserManager.logout(session_id)
    return response.model_dump()


@api.post("/chat")
async def chat(messages: GeminiChatModel):
    # Ensure last message is from user
    if messages.messages[-1].role not in ["user", "human"]:
        return messages
    else:
        return await gemini(messages)

if __name__ == "__main__":
    uvicorn.run(api, port=8080)
