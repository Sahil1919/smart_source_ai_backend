from google import genai
from google.genai import types
from youtube_search import YoutubeSearch
from core.config import settings
from typing import List, Dict

class YouTubeService:
    """Service for YouTube search and video analysis"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """Initialize the YouTube service with API credentials"""
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL_NAME
        self.client = genai.Client(api_key=self.api_key)
    
    def search_videos(self, search_term: str) -> List[Dict]:
        """Search YouTube for videos matching the search term"""
        try:
            results = YoutubeSearch(search_term, max_results=settings.MAX_SEARCH_RESULTS).to_dict()
            return results
        except Exception as e:
            print(f"An error occurred during YouTube search: {e}")
            return []
    
    def summarize_video(self, url: str) -> str:
        """Summarize a YouTube video and return the summary"""
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=url,
                        mime_type="video/*",
                    ),
                    types.Part.from_text(text="summarize this youtube video"),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )
        
        summary = ""
        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=generate_content_config,
            ):
                summary += chunk.text
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"

