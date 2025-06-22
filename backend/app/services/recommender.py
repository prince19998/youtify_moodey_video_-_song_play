import os
import requests
import json
from typing import List
from ..schemas import Video, Recommendation, MoodRecommendation
from .youtube import YouTubeService

class RecommenderService:
    def __init__(self, openrouter_api_key: str):
        self.openrouter_api_key = openrouter_api_key
        self.youtube_service = YouTubeService(os.getenv("YOUTUBE_API_KEY"))
    
    def get_mood_recommendations(self, mood: str) -> MoodRecommendation:
        # Get some popular videos to use as candidates
        candidate_videos = self.youtube_service.get_trending_videos(max_results=20)
        
        # Prepare prompt for LLM
        prompt = self._create_recommendation_prompt(mood, candidate_videos)
        
        # Call OpenRouter API
        response = self._call_openrouter(prompt)
        
        # Parse response
        try:
            recommendations = self._parse_recommendations(response, candidate_videos)
            return MoodRecommendation(mood=mood, videos=recommendations)
        except Exception as e:
            print(f"Error parsing recommendations: {e}")
            # Fallback to random trending videos
            return MoodRecommendation(
                mood=mood,
                videos=[
                    Recommendation(video=video, reason=f"Popular {mood} music")
                    for video in candidate_videos[:5]
                ]
            )
    
    def _create_recommendation_prompt(self, mood: str, videos: List[Video]) -> str:
        video_list = "\n".join([
            f"{idx+1}. {video.title} by {video.channel} (Duration: {video.duration})"
            for idx, video in enumerate(videos)
        ])
        
        return f"""
        You are a music recommendation assistant. Based on the user's current mood ({mood}),
        select 5 videos from the following list that would best match their mood.
        
        For each selected video, provide a brief explanation (10-15 words) of why it matches the mood.
        
        Available videos:
        {video_list}
        
        Please respond with a JSON array where each item has:
        - "index": the number of the selected video (1-based)
        - "reason": why this video matches the mood
        
        Example:
        [
            {{"index": 3, "reason": "Upbeat rhythm perfect for a happy mood"}},
            {{"index": 7, "reason": "Calming melody that enhances relaxation"}}
        ]
        """
    
    def _call_openrouter(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _parse_recommendations(self, response: str, videos: List[Video]) -> List[Recommendation]:
        try:
            recommendations = json.loads(response)
            if not isinstance(recommendations, list):
                raise ValueError("Response is not a list")
            
            result = []
            for rec in recommendations:
                index = rec["index"] - 1  # Convert to 0-based
                if 0 <= index < len(videos):
                    result.append(Recommendation(
                        video=videos[index],
                        reason=rec["reason"]
                    ))
            
            return result
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse recommendations: {e}")