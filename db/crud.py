
from db.database import AsyncMongoClient
from models.api_models import UserSchema, ResponseSchema, Status
from utils.pass_hasher import PasswordUtils
from loguru import logger
from uuid import uuid4
import asyncio

client = AsyncMongoClient("auth-demo")

class UserManager:
    @staticmethod
    async def create_user(user:UserSchema):
        if (await client.db.users.find_one({"username":user.username})):
            return ResponseSchema(status=Status.ERROR, content="username already exists")
        user.password = PasswordUtils.hash_password(user.password)
        result = await client.db.users.insert_one(user.model_dump())
        created = await client.db.users.find_one({"_id":result.inserted_id})
        if created:
            return ResponseSchema(status=Status.SUCCESS, content=client.serialize_doc(created))
        else:
            return ResponseSchema(status=Status.ERROR, content="Some error occurred creating user")
    @staticmethod
    async def login(user:UserSchema, sessions:dict):
        user_instance = await client.db.users.find_one({"username":user.username})
        if not user_instance:
            return ResponseSchema(status=Status.ERROR, content="Username doesn't exist")
        else:
            if PasswordUtils.verify_password(password=user.password, hashed=user_instance["password"]):
                session_id = str(uuid4())
                sessions[session_id]={"username": user.username}
                client.db.sessions.insert_one({
                    "username":user.username,
                    "session_id":session_id
                })
                return ResponseSchema(status=Status.SUCCESS, content={"user":client.serialize_doc(user_instance), "session_id":session_id})
            else:
                return ResponseSchema(status=Status.ERROR, content="Password doesn't match")
    
    @staticmethod
    async def logout(session_id, sessions):
        username = sessions[session_id]["username"]
        result = await client.db.sessions.delete_many({"username":username})
        return ResponseSchema(status=Status.SUCCESS, content={"Logged-Out of all devices"})
    
    @staticmethod
    async def getSessions():
        cursor = client.db.sessions.find({})
        data = {}
        async for session in cursor:
            data[session["session_id"]] = session["username"]
        return data
