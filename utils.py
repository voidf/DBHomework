# from models.Article import *
from fastapi import HTTPException
import math

import jwt
import time
import datetime
import traceback
import hashlib
from typing import Tuple, List, Optional

# from cfg import jwt_token
from fastapi.security import SecurityScopes
from fastapi import Request, HTTPException, Cookie
from pydantic import BaseModel
from GLOBAL import g


class IdModel(BaseModel):
    id: str


def encrypt(s):
    return hashlib.sha256(hashlib.sha256(s.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()


def generate_jwt(user):
    token_dict = {
        'iat': time.time(),  # 1天
        'id': str(user.id)
    }
    return jwt.encode(token_dict,  # payload, 有效载体
                      jwt_token,  # 进行加密签名的密钥
                      algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                      )


def verify_jwt(token):
    try:
        payload = jwt.decode(token, jwt_token, algorithms=['HS256'])
        if payload['iat'] < time.time() - 60*60*24:
            return None, "登入超时"

        user = User.objects(id=payload['id']).first()

        if payload['iat'] < user.pw_updated.timestamp():
            return None, "密码已修改，请使用新密码重新登录"
        if not user:
            return None, "无此用户"
        return user, ""
    except:
        traceback.print_exc()
        return None, "数据错误"

import http.cookies

async def general_before_request(auth: Request):
    """请求预处理，将令牌放入线程作用域g()"""
    try:
        print(auth.client.host, str(datetime.datetime.now()))
        Authorization = auth.headers.get('Authorization', None)
        print(Authorization, auth.cookies)
        if Authorization is None:
            Authorization = auth.cookies.get('Authorization', None)
        if Authorization:
            g().user, g().msg = verify_jwt(Authorization)
            print(f"detect {g().user.name}'s operation...")
        else:
            pass
    except:
        traceback.print_exc()
        raise HTTPException(400, "数据错误")


async def validsign():
    """验证用户是否登录"""
    if not hasattr(g(), 'user'):
        raise HTTPException(401, '此操作需要登陆;'+getattr(g(), 'msg', ""))


def validcall(authority_threshold=0):
    """验证用户权限是否足以进行操作"""
    def validcall_internal():
        if not (g().user.authority & authority_threshold):  # 懒人标记*
            return HTTPException(401, '权限不足')
    return validcall_internal


def resolve_authority(role: str) -> int:
    try:
        return {
            '终审': 0x1000,
            '二审': 0x100,
            '一审': 0x10
        }[role]
    except:
        traceback.print_exc()
        return falseReturn(400, '角色不存在')



def trueReturn(data=None, msg="", code=0):
    return {
        'data': data,
        'msg': msg,
        'status': True
    }


def falseReturn(code=500, msg="", data=None):
    raise HTTPException(code, {
        'data': data,
        'msg': msg,
        'status': False
    })


def get_modify_keys(d: dict) -> dict:
    """自动生成修改参数，一般传入body.dict()来使用"""
    d = fliter_body(d)
    ret = {}
    for k, v in d.items():
        if 'role' == k:
            ret['authority'] = resolve_authority(v)
        elif 'org' == k:
            ret['org'] = chkorg(v)
        elif 'div' == k:
            ret['div'] = chkdiv(v)
        elif 'tag' == k:
            ret['tag'] = chktag(v)
        elif 'tags' == k:
            ret['tags'] = [chktag(i) for i in v]
        elif 'password' == k:
            ret['password'] = encrypt(v)
        else:
            ret[k] = v
    return ret


def fliter_body(d: dict) -> dict:
    """将id和None值元素过滤掉"""
    ret = {}
    for k, v in d.items():
        if k != 'id' and v is not None:
            ret[k] = v
    return ret
