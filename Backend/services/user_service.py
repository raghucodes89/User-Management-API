from database.database import user_collection
from utils.security import hash_password


def create_user(user):
    new_user = {
        "name" : user.name,
        "email" : user.email,
        "password" : hash_password(user.password),
        "role" : user.role
    }
    result = user_collection.insert_one(new_user)

    return {
        "message" : "user  created successfully",
        "user_id" : str(result.inserted_id)
    }