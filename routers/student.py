import datetime
import hashlib
import json
import traceback


from models.学生 import 学生
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Optional
from pydantic import BaseModel

from utils import *

student_route = APIRouter(
    prefix="/student",
    tags=["student"],

    # responses={
    #     401: {"msg": "Unauthorized"},
    #     404: {"msg": "Not found"}
    # }
)


async def require_student_id(student_id: str) -> 学生:
    s = 学生.objects(id_=student_id)
    if not s:
        return falseReturn(404, "指定学号的学生不存在")
    return s[0]


@student_route.get('/{student_id}')
async def student_get(res=Depends(require_student_id)):
    """# 传入需要查询信息的学号，返回学生基本信息

路径参数:

    student_id: str, 学号

返回:
```
{
    学号: str
    姓名: str
    性别: str
    年龄: int
    班级: str
}
```
    """
    return trueReturn(res)


@student_route.get('/')
async def student_get():
    """# 列出所有学生信息

返回:
```
[{
    学号: str
    姓名: str
    性别: str
    年龄: int
    班级: str
},...]
```
    """
    res = 学生.objects()

    return trueReturn(res)


# @student_route.get('/')
# async def student_get2(学号: str):
#     """RESTful api的另外一种表示"""
#     res = 学生.objects(id_=学号)
#     # print('学号')
#     if res:
#         return res[0].json()
#     else:
#         return falseReturn(404, "指定学号的学生不存在")

# class

@student_route.post('/')
async def student_post(student: 学生):
    """# 新增一个学生，id_为索引项，忽略即可，其余按照中文字填，懒得说明了"""
    student.id_ = student.学号
    student.save()
    return trueReturn()


@student_route.put('/{student_id}')
async def student_put(student: 学生, s=Depends(require_student_id)):
    """# 覆写一个学生

路径参数:

    student_id: str, 需要覆写的学生学号

其余填法和新建类似
    """
    s.delete()
    student.save()
    return trueReturn()

class StudentPatch(BaseModel):
    id_: Optional[str]
    学号: Optional[str]
    姓名: Optional[str]
    性别: Optional[str]
    年龄: Optional[int]
    班级: Optional[str]


@student_route.patch('/{student_id}')
async def student_patch(student: StudentPatch, s: 学生=Depends(require_student_id)):
    """# 修改一个学生

路径参数:

    student_id: str, 需要修改的学生学号

其余填法和新建类似，留空则不变
    """
    s.delete()
    student.id_ = student.学号
    s.update(**student.dict(exclude_unset=True))
    s.save()
    return trueReturn()


@student_route.delete('/{student_id}')
async def student_delete(s: 学生=Depends(require_student_id)):
    """# *处决*一个学生

路径参数:

    student_id: str, 需要删除的学生学号
"""
    s.delete()
    return trueReturn()

# @student_route.get('/verify', dependencies=[Depends(validsign)])
# async def verify_auth():
#     return trueReturn(g().user.get_base_info())

# class ChangePassword(BaseModel):
#     old: Optional[str] = ""
#     password: Optional[str] = ""

# @student_route.post('/chpw', dependencies=[
#     Depends(validsign)
# ])
# async def chpw_auth(pw: ChangePassword):
#     old = pw.old
#     password = pw.password
#     user: User = User.objects().first()
#     if not user or not user.valid_password(old):
#         return falseReturn(401, "旧密码不匹配")
#     user.password = encrypt(password)
#     user.pw_updated = datetime.datetime.now()
#     user.save_changes()
#     return trueReturn({
#         'user': user.get_base_info(),
#         'token': generate_jwt(user)
#     })
