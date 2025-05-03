from ..core.config import settings
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..services.url_service import URLService
from ..models.schemas import URLSchema
from typing import Optional
import os

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
    return await url_service.create_short_url(original_url)

@router.get("/{short_url_id}", response_class=HTMLResponse)
async def get_url_info(request: Request, short_url_id: str):
    """
    Display URL information and redirect to the original URL.
    """
    url = await url_service.get_original_url(short_url_id)
    if url:
        # Check if the request wants JSON (API call)
        if request.headers.get("accept") == "application/json":
            return url
        # Otherwise, render the template
        return templates.TemplateResponse("url_info.html", {"request": request, "url": url})
    
    # Raise an HTTP exception
    raise HTTPException(status_code=404, detail="URL not found")

@router.get("/{short_url_id}/redirect")
async def redirect_to_original(short_url_id: str):
    """
    Directly redirect to the original URL without showing the info page.
    """
    url = await url_service.get_original_url(short_url_id)
    if url:
        return RedirectResponse(url.original_url)
    
    raise HTTPException(status_code=404, detail="URL not found")

