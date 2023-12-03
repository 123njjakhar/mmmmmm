'''

from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import random
import os
import re
import config
from Romeo import app 

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


@app.on_message(filters.command("chatbot off", ["/", ".", "?", "-"]) & ~filters.private)
async def chatbotofd(client, message):
    Romeodb = MongoClient(MONGO_DB_URI)    
    Romeo = Romeodb["RomeoDb"]["Romeo"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
           await is_admins(chat_id)
        ):
           return await message.reply_text(
                "You are not admin"
            )
    is_Romeo = Romeo.find_one({"chat_id": message.chat.id})
    if not is_Romeo:
        Romeo.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"Romeo-AI Disabled!")
    if is_Romeo:
        await message.reply_text(f"Romeo-AI Is Already Disabled")
    

@app.on_message(filters.command("chatbot on", ["/", ".", "?", "-"])
async def chatboton(client, message):
    Romeodb = MongoClient(MONGO_DB_URI)    
    Romeo = Romeodb["RomeoDb"]["Romeo"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_Romeo = Romeo.find_one({"chat_id": message.chat.id})
    if not is_Romeo:           
        await message.reply_text(f"Romeo-AI Is Already Enabled")
    if is_Romeo:
        Romeo.delete_one({"chat_id": message.chat.id})
        await message.reply_text(f"Romeo-AI Is Enabled!")
    

@app.on_message(filters.command("chatbot", ["/", ".", "?", "-"])
async def chatbot(client, message):
    await message.reply_text(f"**Usage:**\n/chatbot [on|off] only in groups.")


@app.on_message((filters.text | filters.sticker) & ~filters.private)
async def Romeoai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_DB_URI)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       Romeodb = MongoClient(MONGO_DB_URI)
       Romeo = Romeodb["RomeoDb"]["Romeo"] 
       is_Romeo = Romeo.find_one({"chat_id": message.chat.id})
       if not is_Romeo:
           K = []  
           is_chat = chatai.find({"word": message.text})  
           k = chatai.find_one({"word": message.text})      
           if k:               
               for x in is_chat:
                   K.append(x['text'])          
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "sticker":
                   await message.reply_sticker(f"{hey}")
               if not Yo == "sticker":
                   await message.reply_text(f"{hey}")
   
   if message.reply_to_message:  
       Romeodb = MongoClient(MONGO_DB_URI)
       Romeo = Romeodb["LogicDb"]["Logic"] 
       is_Romeo = Romeo.find_one({"chat_id": message.chat.id})    
       getme = await bot.get_me()
       bot_id = getme.id                             
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_Romeo:                   
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:       
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "sticker":
                       await message.reply_sticker(f"{hey}")
                   if not Yo == "sticker":
                       await message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.sticker:
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})    
               

@app.on_message((filters.sticker | filters.text))
async def Logicstickerai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_DB_URI)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       Romeodb = MongoClient(MONGO_DB_URI)
       Romeo = Romeodb["RomeoDb"]["Romeo"] 
       is_Romeo = Romeo.find_one({"chat_id": message.chat.id})
       if not is_Romeo:
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})      
           k = chatai.find_one({"word": message.text})      
           if k:           
               for x in is_chat:
                   K.append(x['text'])
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "text":
                   await message.reply_text(f"{hey}")
               if not Yo == "text":
                   await message.reply_sticker(f"{hey}")
   
   if message.reply_to_message:
       Romeodb = MongoClient(MONGO_DB_URI)
       Romeo = Romeodb["RomeoDb"]["Romeo"] 
       is_Romeo = Romeo.find_one({"chat_id": message.chat.id})
       getme = await bot.get_me()
       bot_id = getme.id
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_Romeo:                    
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:           
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "text":
                       await message.reply_text(f"{hey}")
                   if not Yo == "text":
                       await message.reply_sticker(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.text:
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
               if not is_chat:
                   toggle.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
           if message.sticker:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})    
               


@app.on_message((filters.text | filters.sticker) & filters.private)
async def Romeoprivate(client: Client, message: Message):

   chatdb = MongoClient(MONGO_DB_URI)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message: 
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")
       

@app.on_message((filters.sticker | filters.text) & filters.private)
async def Romeoprivatesticker(client: Client, message: Message):

   chatdb = MongoClient(MONGO_DB_URI)
   chatai = chatdb["Word"]["WordDb"] 
   if not message.reply_to_message:
       K = []  
       is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "text":
           await message.reply_text(f"{hey}")
       if not Yo == "text":
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "text":
               await message.reply_text(f"{hey}")
           if not Yo == "text":
               await message.reply_sticker(f"{hey}")
               
