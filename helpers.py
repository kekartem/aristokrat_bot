from db import supabase    

async def read_all_managers():
    results = supabase.table('managers').select("*").execute()
    return results


async def save_manager(manager_chat_id):
    data, count = supabase.table('managers').insert({"manager_chat_id": manager_chat_id}).execute()

