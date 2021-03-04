from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from pydantic import BaseModel
from cfg import database_cfg, run_cfg, Admin_mono

def create_fastapi() -> FastAPI:
    # from mongoengine import connect
    app = FastAPI()
    # connect(**database_cfg)

    from routers import master_router
    app.include_router(master_router)

    # from fastapi.middleware.wsgi import WSGIMiddleware
    # from ..app import create_app
    # flask_app = create_app()
    # app.mount('/', WSGIMiddleware(flask_app))
    return app

app = create_fastapi()
if __name__ == '__main__':
    import os
    # from models.User import User, encrypt
    # from models.Base import Base
    # if not os.path.exists('.init'):
    #     Base.objects().delete()
    #     u = User.get_or_create(Admin_mono['name'], password=encrypt(Admin_mono['pw']))
    #     u.authority = 0x1110
    #     u.save_changes()
    #     with open('.init', 'w') as f: pass
    # uvicorn.run(app, **run_cfg)
    from models.学生 import 学生
    from models.课程 import 课程
    from models.选课 import 选课
    s = 学生(
        学号='114514',
        姓名='hjagfkagjs',
        性别='?',
        年龄=24,
        班级='sad'
    )

    s.save()
    print(学生.objects())