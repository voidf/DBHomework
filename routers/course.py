import datetime
import hashlib
import json
import traceback


from models.课程 import 课程
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Optional
from pydantic import BaseModel

from utils import *

course_route = APIRouter(
    prefix="/course",
    tags=["course"],

    # responses={
    #     401: {"msg": "Unauthorized"},
    #     404: {"msg": "Not found"}
    # }
)


async def require_course_id(course_id: str) -> 课程:
    s = 课程.objects(id_=course_id)
    if not s:
        return falseReturn(404, "指定编号的课程不存在")
    return s[0]


@course_route.get('/{course_id}')
async def course_get(res=Depends(require_course_id)):
    """# 查"""
    return trueReturn(res)


@course_route.get('/')
async def course_get():
    """# 列出"""
    res = 课程.objects()
    return trueReturn(res)

@course_route.post('/')
async def course_post(course: 课程):
    """# 增"""
    course.id_ = course.课程编号
    course.save()
    return trueReturn()


@course_route.put('/{course_id}')
async def course_put(course: 课程, s=Depends(require_course_id)):
    """# 改：覆写"""
    s.delete()
    course.save()
    return trueReturn()

class CoursePatch(BaseModel):
    id_: Optional[str]
    课程编号: Optional[str]
    名称: Optional[str]
    学分: Optional[int]

@course_route.patch('/{course_id}')
async def course_patch(course: CoursePatch, s=Depends(require_course_id)):
    """# 改：修改"""
    s.delete()
    course.id_ = course.课程编号
    s.update(**course.dict(exclude_unset=True))
    s.save()
    return trueReturn()

@course_route.delete('/{course_id}')
async def course_delete(s=Depends(require_course_id)):
    """# 删"""
    s.delete()
    return trueReturn()
