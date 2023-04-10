from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from src.config.settings import general

from src.routers.users import user_router
from src.routers.posts import post_router


def include_router(app: FastAPI):
    app.include_router(user_router, prefix='/api/v1/users')
    app.include_router(post_router, prefix='/api/v1/posts')
    pass


def add_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(title=general.project_name, version=general.version)
    include_router(app)
    add_middleware(app)

    @app.get("/helloworld_check")
    async def hello_world() -> Response:
        return Response(status_code=status.HTTP_200_OK)

    return app


app = create_app()
