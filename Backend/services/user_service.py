from database.database import user_collection
from utils.security import hash_password, verify_password, create_access_token
from bson import ObjectId

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

def login_user(user):
        existing_user = user_collection.find_one({"email" : user.email})

        if not existing_user:
            return {"message" : "User not found"}

        if not verify_password(user.password, existing_user["password"]):
            return {"message" : "Invalid email or password"}

        access_token = create_access_token({
            "user_id" : str(existing_user["_id"]),
            "role" : existing_user["role"]
        })    

        return {
            "message" : "Login Successful",
            "access_token" : access_token,
            "token_type" : "bearer"
        }


def get_all_users():
    users = list(user_collection.find())

    for user in users:
        user["_id"] = str(user["_id"])
        user.pop("password",None)

    return users


def get_user_by_id(user_id):
    user = user_collection.find_one({
        "_id" : ObjectId(user_id)
    })
    
    if not user:
        return None

    user["_id"] = str(user["_id"])
    user.pop("password", None)

    return user
