import datetime
import hashlib
import json
import traceback


from models.选课 import 选课
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Optional
from pydantic import BaseModel

from utils import *

selection_route = APIRouter(
    prefix="/selection",
    tags=["selection"],

    # responses={
    #     401: {"msg": "Unauthorized"},
    #     404: {"msg": "Not found"}
    # }
)


async def require_selection_id(selection_id: str) -> 选课:
    s = 选课.objects(id_=selection_id)
    if not s:
        return falseReturn(404, "指定id的选课不存在")
    return s[0]


@selection_route.get('/{selection_id}')
async def selection_get(res=Depends(require_selection_id)):
    """# 查"""
    return trueReturn(res)


@selection_route.get('/')
async def selection_get():
    """# 列出"""
    res = 选课.objects()
    return trueReturn(res)

import uuid

@selection_route.post('/')
async def selection_post(selection: 选课):
    """# 增"""
    selection.id_ = str(uuid.uuid1()).replace('-','')
    selection.save()
    return trueReturn()


@selection_route.put('/{selection_id}')
async def selection_put(selection: 选课, s=Depends(require_selection_id)):
    """# 改：覆写"""
    selection.id_ = s.id_
    s.delete()
    selection.save()
    return trueReturn()

class selectionPatch(BaseModel):
    id_: Optional[str]
    学号: Optional[str]
    课程编号: Optional[str]
    成绩: Optional[int]

@selection_route.patch('/{selection_id}')
async def selection_patch(selection: selectionPatch, s=Depends(require_selection_id)):
    """# 改：修改"""
    s.delete()
    selection.id_ = None
    s.update(**selection.dict(exclude_unset=True))
    s.save()
    return trueReturn()

@selection_route.delete('/{selection_id}')
async def selection_delete(s=Depends(require_selection_id)):
    """# 删"""
    s.delete()
    return trueReturn()
