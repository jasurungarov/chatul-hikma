from database import save_user_to_db

def register_user(chat_id: int, name: str, location: dict):
    user = {"chat_id": chat_id, "name": name, "location": location}
    save_user_to_db(user)