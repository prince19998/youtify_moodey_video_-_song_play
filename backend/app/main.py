import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from .services.youtube import YouTubeService
from .services.recommender import RecommenderService
from .models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Youtify Clone")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

def format_number(value):
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

templates.env.filters["format_number"] = format_number

def linebreaks(value):
    if not isinstance(value, str):
        return value
    return value.replace('\n', '<br>')

templates.env.filters["linebreaks"] = linebreaks

# Services
youtube_service = YouTubeService(os.getenv("YOUTUBE_API_KEY"))
recommender_service = RecommenderService(os.getenv("OPENROUTER_API_KEY"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get mood-based recommendations
    mood = "happy"  # In a real app, this would be detected or selected by user
    recommendations = recommender_service.get_mood_recommendations(mood)
    
    # Get trending videos
    trending = youtube_service.get_trending_videos()
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "recommendations": recommendations,
        "trending": trending
    })

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = ""):
    if not q:
        return RedirectResponse("/")
    
    results = youtube_service.search_videos(q)
    return templates.TemplateResponse("search.html", {
        "request": request,
        "results": results,
        "query": q
    })

@app.get("/watch/{video_id}", response_class=HTMLResponse)
async def watch(request: Request, video_id: str):
    video = youtube_service.get_video_details(video_id)
    related = youtube_service.get_related_videos(video_id)
    
    return templates.TemplateResponse("player.html", {
        "request": request,
        "video": video,
        "related": related
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)