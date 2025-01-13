from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import DocumentRoutes
from app.core.initializer import AppInitializer
from app.db.database import database_instance
from app.dependencies import Dependency


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5174"],  # Adjust to your frontend URL
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    initializer = AppInitializer(app, database_instance.database)
    initializer.initialize()
    dependency = Dependency(initializer.db)

    # Include routers
    document_routes = DocumentRoutes(dependency = dependency)
    app.include_router(document_routes.router)
    return app

app = create_app()
