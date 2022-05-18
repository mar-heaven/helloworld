import re
import datetime
import hashlib
import random

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from faker import Faker

from helloworld.modles.user import UserInDB, UserLogin

PROJECTION = {"_id": 0, "user_id": 1, "phone": 1, "username": 1}
TABLE_NAME = "users"
ID_TABLE_NAME = "user"

f = Faker(locale='zh_CN')


def _get_fake_name():
    return f.name()


async def check_user(
    db: AsyncIOMotorDatabase,
    user: UserInDB
):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, str(user.phone))
    if not res:
        return "手机号不合法"
    if user.password != user.password_repeat:
        return "两次密码不一致！"
    filter_ = {
        "phone": user.phone,
    }
    user_instance = await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)
    if user_instance:
        return "该用户已被注册！"
    return False


async def create_user(
    db: AsyncIOMotorDatabase,
    user: UserInDB
) -> None:
    """
    phone: int
    password: str
    """
    id_instance = await db.id_collection.find_one_and_update(filter={'system': ID_TABLE_NAME},
                                                             update={'$inc': {'max_id': 1}},
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)

    user_id = id_instance['max_id']
    age = random.randint(0, 2)
    name = _get_fake_name()
    user_instance = {
        "user_id": user_id,
        "phone": user.phone,
        "age": age,
        "username": name,
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
        "create_at": datetime.datetime.now()
    }
    await db[TABLE_NAME].insert_one(user_instance)


async def login(
    db: AsyncIOMotorDatabase,
    user: UserLogin
) -> dict:
    filter_ = {
        "phone": user.phone,
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
    }
    return await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)


async def get_user(
    db: AsyncIOMotorDatabase,
    user_id: int
) -> dict:
    filter_ = {
        "user_id": user_id,
    }
    return await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)
