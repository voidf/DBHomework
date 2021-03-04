import datetime
import hashlib
import json
import traceback


from models.User import User, encrypt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Optional
from pydantic import BaseModel

from utils import *

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"],
    
    # responses={
    #     401: {"msg": "Unauthorized"},
    #     404: {"msg": "Not found"}    
    # }
)

class login_form(BaseModel):
    username: Optional[str] = ''
    password: Optional[str] = ''

@auth_route.post('/signin')
async def signin_auth(data: login_form, req: Request, rsp: Response):
    name = data.username.strip()
    password = data.password
    user: User = User.objects(name=name).first()
    if not user or not user.valid_password(password):
        return falseReturn(404, "找不到该用户")
    if not user.status:
        return falseReturn(401, "用户已被停用，请联系管理员")
    if user.org and not user.org.status:
        return falseReturn(401, "该用户所属组织已被停用，请联系管理员")
    userinfo = user.get_base_info()
    user.modify(
        last_ip=req.client.host,
        last_login=datetime.datetime.now()
    )
    tk = generate_jwt(user)
    rsp.set_cookie("Authorization", tk, 86400)
    return trueReturn({
        'user': userinfo,
        'token': tk,
    })

class ChangeInfo(BaseModel):
    tel: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    org: Optional[str] = None

@auth_route.post('/chinfo', dependencies=[Depends(validsign)])
async def chinfo_auth(info: ChangeInfo, r: Request):

    modify_keys = {}
    for k, v in info.dict().items():
        if v is not None:
            if k == 'org':
                modify_keys[k] = Org.objects(id=v).first()
            else:
                modify_keys[k] = v
    g().user.modify(**modify_keys)
    g().user.last_ip = r.client.host
    g().user.save_changes()
    return trueReturn()


@auth_route.get('/verify', dependencies=[Depends(validsign)])
async def verify_auth():
    return trueReturn(g().user.get_base_info())

class ChangePassword(BaseModel):
    old: Optional[str] = ""
    password: Optional[str] = ""

@auth_route.post('/chpw', dependencies=[
    Depends(validsign)
])
async def chpw_auth(pw: ChangePassword):
    old = pw.old
    password = pw.password
    user: User = User.objects().first()
    if not user or not user.valid_password(old):
        return falseReturn(401, "旧密码不匹配")
    user.password = encrypt(password)
    user.pw_updated = datetime.datetime.now()
    user.save_changes()
    return trueReturn({
        'user': user.get_base_info(),
        'token': generate_jwt(user)
    })
