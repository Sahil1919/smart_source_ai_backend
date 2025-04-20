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
            results = YoutubeSearch(
                search_term, max_results=settings.MAX_SEARCH_RESULTS
            ).to_dict()
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
                    types.Part.from_text(
                        text=(
                            "Summarize this YouTube video by extracting the key topics with timestamps.\n\n"
                            "Format the output in **Markdown** with the following structure:\n\n"
                            "- **`00:00` Introduction to the topic**\n"
                            "  A short paragraph summarizing what is discussed in this section.\n\n"
                            "- **`01:45` Main Concept A**\n"
                            "  A few sentences explaining the concept, examples, or discussion happening in this part.\n\n"
                            "- **`04:10` Demonstration/Example**\n"
                            "  Explain what’s demonstrated here, what tools or techniques are shown, and key insights.\n\n"
                            "- **`08:00` Conclusion and Takeaways**\n"
                            "  Summarize the final thoughts and what the viewer should remember.\n\n"
                            "Use Markdown formatting only. Do not add anything outside this format. Make sure each bullet has a clear timestamp, a bolded title, and a short description below."
                        )
                    ),
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


# def summarize_video(self, url: str) -> str:
#     """Summarize a YouTube video with timestamps in Markdown format and return the summary"""
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_uri(
#                     file_uri=url,
#                     mime_type="video/*",
#                 ),
#                 types.Part.from_text(
#                     text=(
#                         "Summarize this YouTube video by extracting key points with timestamps.\n"
#                         "Format the output in **Markdown** using the structure:\n\n"
#                         "### Timestamp Summary\n\n"
#                         "- `00:00` Introduction to the topic\n"
#                         "- `01:45` Explanation of main concept A\n"
#                         "- `04:10` Demonstration/example\n"
#                         "- `08:00` Conclusion and key takeaways\n\n"
#                         "Keep the summary concise but informative. Return only the markdown."
#                     )
#                 ),
#             ],
#         ),
#     ]

#     generate_content_config = types.GenerateContentConfig(
#         temperature=1,
#         top_p=0.95,
#         top_k=40,
#         max_output_tokens=8192,
#         response_mime_type="text/markdown",  # Changed to markdown
#     )

#     summary = ""
#     try:
#         for chunk in self.client.models.generate_content_stream(
#             model=self.model_name,
#             contents=contents,
#             config=generate_content_config,
#         ):
#             summary += chunk.text
#         return summary
#     except Exception as e:
#         print(f"Error generating summary: {e}")
#         return f"Error generating summary: {str(e)}"
