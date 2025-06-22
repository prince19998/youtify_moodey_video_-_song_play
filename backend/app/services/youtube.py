import os
import requests
from typing import List, Optional
from ..schemas import Video

class YouTubeService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Video]:
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        videos = []
        for item in data.get("items", []):
            video = Video(
                id=item["id"]["videoId"],
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
                channel=item["snippet"]["channelTitle"],
                duration="N/A"
            )
            videos.append(video)
        
        # Get durations for videos
        video_ids = [video.id for video in videos]
        durations = self._get_video_durations(video_ids)
        
        for video in videos:
            video.duration = durations.get(video.id, "N/A")
        
        return videos
    
    def get_video_details(self, video_id: str) -> Video:
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": video_id,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data.get("items"):
            return None
        
        item = data["items"][0]
        return Video(
            id=item["id"],
            title=item["snippet"]["title"],
            description=item["snippet"]["description"],
            thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
            channel=item["snippet"]["channelTitle"],
            duration=item["contentDetails"]["duration"],
            views=int(item["statistics"].get("viewCount", 0))
        )
    
    def get_related_videos(self, video_id: str, max_results: int = 5) -> List[Video]:
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "relatedToVideoId": video_id,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        videos = []
        for item in data.get("items", []):
            video = Video(
                id=item["id"]["videoId"],
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
                channel=item["snippet"]["channelTitle"],
                duration="N/A"
            )
            videos.append(video)
        
        return videos
    
    def get_trending_videos(self, max_results: int = 10) -> List[Video]:
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet,contentDetails,statistics",
            "chart": "mostPopular",
            "maxResults": max_results,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        videos = []
        for item in data.get("items", []):
            video = Video(
                id=item["id"],
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
                channel=item["snippet"]["channelTitle"],
                duration=item["contentDetails"]["duration"],
                views=int(item["statistics"].get("viewCount", 0))
            )
            videos.append(video)
        
        return videos
    
    def _get_video_durations(self, video_ids: List[str]) -> dict:
        url = f"{self.base_url}/videos"
        params = {
            "part": "contentDetails",
            "id": ",".join(video_ids),
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        durations = {}
        for item in data.get("items", []):
            durations[item["id"]] = item["contentDetails"]["duration"]
        
        return durations