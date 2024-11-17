from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.user import user_route, user_schema
from app.department import department_route
from app.classroom import classroom_route
from app.subject import subject_route
from app.semester import semester_route
from app.staff import staff_route
from app.schedule import schedule_route
from app.database import engine
from app.core.logger import logger

# Create all tables for the first time
user_schema.Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI()

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_route.route)
app.include_router(department_route.route)
app.include_router(classroom_route.route)
app.include_router(semester_route.route)
app.include_router(subject_route.route)
app.include_router(staff_route.route)
app.include_router(schedule_route.route)


# Global error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"unhandled error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "internal server error occurred.",
            "error": str(exc),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "validation error", "error": exc.errors()},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# Event handlers for startup and shutdown
# @app.on_event("startup")
# async def on_startup():
#     logger.info("Starting up the FastAPI application...")


# @app.on_event("shutdown")
# async def on_shutdown():
#     logger.info("Shutting down the FastAPI application...")
