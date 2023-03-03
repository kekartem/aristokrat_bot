import re
from db import database


async def create_tables():
    await database.execute('''CREATE TABLE IF NOT EXISTS managers (
        id SERIAL PRIMARY KEY,
        manager_chat_id TEXT NOT NULL
    );''')
    

async def read_all_managers():
    results = await database.fetch_all('SELECT * FROM managers')
    print('AAAAAAAAAAAAAAAAAAAAA', results)
    return results


async def save_manager(manager_chat_id):
    await database.execute(
        'INSERT INTO managers(manager_chat_id) VALUES (:manager_chat_id)',
        values={'manager_chat_id': manager_chat_id})

