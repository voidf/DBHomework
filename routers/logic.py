import datetime
import hashlib
import json
import traceback


from models.选课 import 选课
from models.课程 import 课程
from models.学生 import 学生
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Optional
from pydantic import BaseModel

from utils import *

logic_route = APIRouter(
    prefix="/logic",
    tags=["logic"],
)

async def require_student_id(student_id: str) -> 学生:
    s = 学生.objects(id_=student_id)
    if not s:
        return falseReturn(404, "指定学号的学生不存在")
    return s[0]


@logic_route.get('/showall/{student_id}')
async def a3(s=Depends(require_student_id)):
    """# 根据输入的学号，查询并显示该学生的姓名、选修的所有课程的名称及成绩"""
    selections = 选课.objects(学号=s.学号)
    output = {}
    for i in selections:
        c = 课程.objects(id_=i.课程编号)[0]
        output[c.名称] = i.成绩
    return trueReturn(
        {
            '姓名': s.姓名,
            '选修情况':output
        }
    )

@logic_route.get('/avg/{student_id}')
async def a4(s=Depends(require_student_id)):
    """# 根据给定的学号，查询并显示该生的平均成绩"""
    selections = 选课.objects(学号=s.学号)
    output = {}
    tot = 0
    ctr = 0
    for i in selections:
        ctr+=1
        tot+=i.成绩
    if ctr == 0: ctr = 1
    return trueReturn(
        {
            '平均成绩': tot/ctr
        }
    )