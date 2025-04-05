# Smart Source AI Backend

A powerful API for web search and YouTube video analysis powered by AI.

## Overview

Smart Source AI Backend is a FastAPI application that provides intelligent search capabilities and YouTube video analysis. It leverages advanced language models to extract meaningful information from web pages and summarize YouTube videos.

## Features

- **Web Search:** Perform web searches and get AI-powered answers from relevant sources.
- **YouTube Search:** Discover YouTube videos related to your query.
- **YouTube Video Summarization:** Generate AI-driven summaries of YouTube videos.
- **RESTful API:** Clean, well-documented API endpoints.
- **Scalable Architecture:** Modular design for easy maintenance and extension.

## Tech Stack

- **FastAPI:** High-performance web framework
- **Groq API:** LLM for web search analysis (using LLama 3.1)
- **Google Gemini API:** For YouTube video summarization
- **Goose3:** Web content extraction
- **YouTube Search:** YouTube video discovery

## Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/smart_source_ai_backend.git
   cd smart_source_ai_backend
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory with:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_MODEL_NAME=llama-3.1-8b-instant
   GEMINI_MODEL_NAME=gemini-2.0-flash
   MAX_SEARCH_RESULTS=4
   ```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Web Search
- `POST /api/search/`: Perform a web search
```json
{
    "query": "climate change solutions"
}
```

#### YouTube
- `POST /api/youtube/search`: Search for videos
- `POST /api/youtube/summarize`: Generate video summary
```json
{
    "video_url": "https://www.youtube.com/watch?v=example"
}
```

## Development

### Project Structure
```
smart_source_ai_backend/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   │   └── schemas/
│   └── services/
├── core/
│   ├── config.py
│   ├── server.py
├── main.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

## Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Run from project root
- **API Key Errors**: Verify .env configuration
- **Rate Limits**: Implement request delays/chunking

## License

MIT License

## Contributors

- Sahil Shaikh
- Priyanshu Dubey
- Harsh Masaye
- Ayan Shah

## Acknowledgements

- FastAPI
- Groq
- Google Gemini
- Goose3

Feel free to contribute by opening issues or submitting pull requests!