from fastapi import APIRouter, HTTPException

from helloworld import crud
from helloworld.db.database import get_mongo
from helloworld.modles.user import UserInDB
from helloworld.modles.response import Response

router = APIRouter()


@router.post(
    "/register/", response_model=Response
)
async def register(user: UserInDB):
    """ 用户注册"""
    db = get_mongo()

    check_validation = await crud.user.check_user(db, user)
    if check_validation:
        raise HTTPException(status_code=400, detail=check_validation)
    await crud.user.create_user(db, user)
    return Response(msg="注册成功", status=201)


@router.get(
    "/user/{user_id}"
)
async def get_user(user_id: int):
    """ 获取用户信息"""
    db = get_mongo()
    user = await crud.user.get_user(db, user_id)
    return {"user_info": user, 'status': 200}
