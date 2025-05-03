from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from .endpoints import urls
from .core.config import settings

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener API built with FastAPI and MongoDB.",
    version="1.0.0",
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the URL endpoints
app.include_router(urls.router)
# Include other routers as needed

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page - redirects to URL creation form
    """
    return templates.TemplateResponse("create_url.html", {"request": request})

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

