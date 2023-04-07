from db import supabase_client    

async def read_all_managers():
    results = supabase_client.table('managers').select("*").execute()
    return results


async def save_manager(manager_chat_id):
    data, count = supabase_client.table('managers').insert({"manager_chat_id": manager_chat_id}).execute()


async def update():
    results = supabase_client.table('managers').select("*").execute()
    return results
