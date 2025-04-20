from langchain_groq import ChatGroq
from goose3 import Goose
from googlesearch import search
from core.config import settings
from typing import List, Dict


class SearchService:
    """Service for web search operations"""

    def __init__(self, api_key: str = None, model_name: str = None):
        """Initialize the search service with API credentials"""
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model_name = model_name or settings.GROQ_MODEL_NAME
        self.llm = ChatGroq(groq_api_key=self.api_key, model_name=self.model_name)
        self.goose = Goose()

    def web_search(self, query: str) -> List[str]:
        """Search top web results related to query"""
        search_result = search(query, settings.MAX_SEARCH_RESULTS)
        return list(search_result)

    def extract_text(self, top_links: List[str]) -> List[str]:
        """Extract the text from web pages"""
        article_text = []
        for url in top_links:
            if url:
                try:
                    article = self.goose.extract(url)
                    article_text.append(article.cleaned_text)
                except Exception as e:
                    print(f"Could not reach {url}: {str(e)}")

        return article_text

    def get_answers(self, query: str, article_texts: List[str]) -> List[str]:
        """Get answers from the LLM based on article texts"""
        answers = []
        max_chars = 2500  # Conservative limit to stay under token limits

        for text in article_texts:
            if not text.strip():
                continue

            try:
                # Truncate text to reduce token count
                truncated_text = text[:max_chars]

                ans = self.llm.invoke(
                    f"""paragraph: {truncated_text} question: {query} prompt: Based solely on the paragraph below, answer the question in your own words. Respond in 500 words using Markdown format. Do not repeat or restate the paragraph or question. Only provide a concise, informative answer derived from the paragraph. If the paragraph does not contain the answer, use your own reasoning to respond."""
                )
                answers.append(ans.content)

            except Exception as e:
                error_msg = str(e)
                print(f"Error getting answer: {error_msg}")

                # If we hit rate limits, try with an even smaller text
                if "rate_limit_exceeded" in error_msg:
                    try:
                        # Try with half the size
                        truncated_text = text[: max_chars // 2]
                        ans = self.llm.invoke(
                            f"""paragraph: {truncated_text} question: {query} prompt: Based solely on the paragraph below, answer the question in your own words. Respond in 500 words using Markdown format. Do not repeat or restate the paragraph or question. Only provide a concise, informative answer derived from the paragraph. If the paragraph does not contain the answer, use your own reasoning to respond."""
                        )
                        answers.append(ans.content)
                    except Exception as e2:
                        answers.append(
                            f"Could not process this source due to API limitations: {str(e2)[:100]}..."
                        )
                else:
                    answers.append(f"Error processing source: {error_msg[:100]}...")

        return answers

    def perform_search_operation(self, query: str) -> Dict:
        """Perform the complete search operation"""
        top_links = self.web_search(query)
        article_texts = self.extract_text(top_links)
        answers = self.get_answers(query, article_texts)

        return {"query": query, "links": top_links, "answers": answers}
