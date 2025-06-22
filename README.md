# Youtify Clone

A full-stack music and video streaming web application inspired by YouTube Music, built with FastAPI, Jinja2, SQLAlchemy, and modern frontend technologies.

## Features
- Search for YouTube videos and music
- Watch videos in an embedded player
- Mood-based music recommendations using OpenRouter LLM
- Trending video discovery
- User and watch history database (SQLAlchemy models)
- Responsive frontend with custom CSS and JS

## Project Structure
```
youtify-clone/
  backend/
    app/
      main.py            # FastAPI app entrypoint
      models.py          # SQLAlchemy models (User, History)
      schemas.py         # Pydantic schemas
      services/
        youtube.py       # YouTube API integration
        recommender.py   # Mood-based recommender using LLM
    requirements.txt     # Backend dependencies
  frontend/
    static/
      css/style.css      # Main stylesheet
      js/main.js         # Main JavaScript
      favicon.ico        # (Add your favicon here)
    templates/
      base.html          # Base template
      home.html          # Home page
      search.html        # Search results
      player.html        # Video player
  youtify.db             # SQLite database
  README.md              # This file
```

## Requirements
- Python 3.8+
- YouTube Data API v3 key
- OpenRouter API key (for recommendations)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd music_app/youtify-clone
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   pip install -r backend/requirements.txt
   ```
4. **Set up environment variables:**
   Create a `.env` file in the root or backend directory with:
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   DATABASE_URL=sqlite:///../youtify.db
   ```

## Running the App
1. **Start the FastAPI backend:**
   ```bash
   uvicorn backend.app.main:app --reload
   ```
2. **Open your browser and go to:**
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Custom Jinja2 Filters
- `format_number`: Formats numbers with commas (e.g., 10000 → 10,000)
- `linebreaks`: Converts newlines to `<br>` in descriptions

## Notes
- Add a `favicon.ico` to `frontend/static/` for a custom browser tab icon.
- The app uses SQLite by default; you can change the `DATABASE_URL` for other databases.
- API keys are required for full functionality.

## License
MIT License 