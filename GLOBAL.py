import contextvars
import types
request_global = contextvars.ContextVar(
    "request_global",
    default=types.SimpleNamespace()
)

import os
# WORKDIR = os.curdir 
FSDBDIR = 'FSDBSINGLE/' # 文件系统模拟数据库初始目录
if not os.path.exists(FSDBDIR):
    os.mkdir(FSDBDIR)
# FSDBINDEX = '_oid' # pydantic不支持

def g():
    return request_global.get()