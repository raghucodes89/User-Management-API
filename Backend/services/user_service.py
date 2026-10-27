from fastapi import HTTPException
from database.database import user_collection
from utils.security import hash_password, verify_password, create_access_token
from bson import ObjectId

def create_user(user):
    existing_user = user_collection.find_one({
        "email" : user["email"]
    })

    if existing_user :
        raise HTTPException(
            status_code=400,
            detail = "Email already registered"
        )
    
    individual_id = f"{user["department_code"]}-{user["employee_number"]}"

    new_user = {
        "name": user["name"],
        "email": user["email"],
        "password": hash_password(user["password"]),
        "role": user["role"],
        "department_code": user["department_code"],
        "employee_number": user["employee_number"],
        "individual_id": individual_id,
        "profile_photo": user.get("profile_photo")
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
    if not ObjectId.is_valid(user_id):
        return None

    user = user_collection.find_one({
        "_id" : ObjectId(user_id)
    })
    
    if not user:
        return None

    user["_id"] = str(user["_id"])
    user.pop("password", None)

    return user


def update_user(user_id, data):
    update_data = {
        key : value 
        for key, value in data.model_dump().items()
    }

    result = user_collection.update_one(
        {"_id" : ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None
    
    return get_user_by_id(user_id)   


def delete_user(user_id):
    result = user_collection.delete_one({
        "_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        return False

    return True  


def change_password(user_id: str, current_password: str, new_password: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return None

    if not verify_password(current_password,user["password"]):
        raise ValueError("Current password is incorrect")


    new_hashed_password  =  hash_password(new_password)

    user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": new_hashed_password}}
    )

    return True

def admin_change_password(user_id: str, new_password: str):
    user = user.collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return None

    new_hashed_password = hash_password(new_password)

    user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": new_hashed_password}}
    )

    return True