from fastapi import APIRouter
from src.web.api.monitoring.views import router as monitoring_router
from src.web.api.users.views import router as users_router
from src.web.api.posts.views import router as posts_router


api_router = APIRouter()
api_router.include_router(monitoring_router, prefix="", tags=["Monitoring"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(posts_router, prefix="/posts", tags=["Posts"])