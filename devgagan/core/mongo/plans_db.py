# ---------------------------------------------------
# File Name: plans_db.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import datetime
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB
 
# Assuming MONGO_DB is loaded from a config file/env
MONGO_DB = os.environ.get("MONGO_DB") 

if MONGO_DB: # <--- ADD THIS CHECK
    mongo = MongoCli(MONGO_DB) # Only initialize if the URI is set
else:
    # Create a dummy/empty class to prevent crashes in other functions
    class DummyMongo:
        def __init__(self):
            print("WARNING: Database functions disabled.")

        # Add methods that the rest of the file uses, returning None or empty data
        def check_and_remove_expired_users(self):
            return
        
        # You'll need to define all methods used later in this file
        # (e.g., plans.check_and_remove_expired_users, if that's what's used)

    mongo = DummyMongo()
db = mongo.premium
db = db.premium_db
 
async def add_premium(user_id, expire_date):
    data = await check_premium(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"expire_date": expire_date}})
    else:
        await db.insert_one({"_id": user_id, "expire_date": expire_date})
 
async def remove_premium(user_id):
    await db.delete_one({"_id": user_id})
 
async def check_premium(user_id):
    return await db.find_one({"_id": user_id})
 
async def premium_users():
    id_list = []
    async for data in db.find():
        id_list.append(data["_id"])
    return id_list
 
async def check_and_remove_expired_users():
    current_time = datetime.datetime.utcnow()
    async for data in db.find():
        expire_date = data.get("expire_date")
        if expire_date and expire_date < current_time:
            await remove_premium(data["_id"])
            print(f"Removed user {data['_id']} due to expired plan.")
 
