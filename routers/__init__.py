from fastapi import APIRouter, Depends
from utils import general_before_request
master_router = APIRouter(
    prefix="/api/v2",
    tags=["master"],
    dependencies=[Depends(general_before_request)]
)

from .student import student_route
from .course import course_route
from .selection import selection_route
from .logic import logic_route

master_router.include_router(student_route)
master_router.include_router(course_route)
master_router.include_router(selection_route)
master_router.include_router(logic_route)

# from .auth import auth_route

# from .org import org_route
# from .user import user_route
# from .tag import tag_route
# from .div import div_route
# from .contrib import contrib_route
# from .article import article_route

# from .initialize import initialize_route

# master_router.include_router(auth_route)
# master_router.include_router(org_route)
# master_router.include_router(user_route)
# master_router.include_router(tag_route)
# master_router.include_router(div_route)
# master_router.include_router(contrib_route)
# master_router.include_router(article_route)

# master_router.include_router(initialize_route)