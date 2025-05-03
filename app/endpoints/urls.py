import logging
import os
from typing import Optional
from core.config import settings
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from services.url_service import URLService
from models.schemas import URLSchema

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/urls", tags=["URLs"])
url_service = URLService()

# Set up Jinja2 templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/create", response_class=HTMLResponse)
async def create_url_form(request: Request):
    """
    Display the URL creation form.
    """
    return templates.TemplateResponse("create_url.html", {"request": request})

@router.post("/create", response_model=URLSchema)
async def create_short_url(original_url: str):
    """
    Create a shortened URL.
    """
    try:
        logger.debug(f"Received request to create short URL for: {original_url}")
        
        if not original_url:
            logger.error("No URL provided")
            raise HTTPException(status_code=400, detail="URL is required")
        
        url = await url_service.create_short_url(original_url)
        logger.debug(f"Created short URL: {url.dict()}")
        return url
    except Exception as e:
        logger.error(f"Error creating short URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create short URL: {str(e)}")

@router.get("/{short_url_id}", response_class=HTMLResponse)
async def get_url_info(request: Request, short_url_id: str):
    """
    Display URL information and redirect to the original URL.
    """
    try:
        logger.debug(f"Looking up URL with ID: {short_url_id}")
        url = await url_service.get_original_url(short_url_id)
        
        if url:
            logger.debug(f"Found URL: {url.dict()}")
            # Check if the request wants JSON (API call)
            if request.headers.get("accept") == "application/json":
                return JSONResponse(content=url.dict())
            # Otherwise, render the template
            return templates.TemplateResponse("url_info.html", {"request": request, "url": url})
        
        logger.error(f"URL not found: {short_url_id}")
        raise HTTPException(status_code=404, detail="URL not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving URL: {str(e)}")

@router.get("/{short_url_id}/redirect")
async def redirect_to_original(short_url_id: str):
    """
    Directly redirect to the original URL without showing the info page.
    """
    try:
        logger.debug(f"Redirecting URL with ID: {short_url_id}")
        url = await url_service.get_original_url(short_url_id)
        
        if url:
            logger.debug(f"Redirecting to: {url.original_url}")
            return RedirectResponse(url.original_url)
        
        logger.error(f"URL not found for redirect: {short_url_id}")
        raise HTTPException(status_code=404, detail="URL not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error redirecting URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error redirecting URL: {str(e)}")

