from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return request.app.state.templates.TemplateResponse("search.html", {"request": request})
