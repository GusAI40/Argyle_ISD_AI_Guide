# 🎓 Argyle ISD AI Guide

An intelligent Q&A assistant for the Argyle Independent School District that allows citizens to ask natural language questions about the district and get instant answers with source citations.

## Features

- 🔍 **Smart Search**: Powered by OpenAI's GPT-4o for natural language understanding
- 📄 **Complete Coverage**: Crawls all public pages from argyleisd.com
- 📚 **PDF Support**: Includes district handbooks, calendars, and policy documents
- 🔗 **Source Citations**: Every answer includes clickable links to original sources
- ⚡ **Real-time**: Instant responses with caching for better performance
- 🎯 **Citizen-focused**: Built specifically for parents, students, and staff

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Get your API keys from:

- [Firecrawl](https://www.firecrawl.dev/) - for web crawling
- [OpenAI](https://platform.openai.com/) - for AI responses

Set them as environment variables:

```bash
export FIRECRAWL_API_KEY="your-firecrawl-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

Or create a `.env` file:

```
FIRECRAWL_API_KEY=your-firecrawl-api-key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Example Questions

Try asking questions like:

- "What are the school hours for Argyle Elementary?"
- "How do I enroll my child in kindergarten?"
- "When is the next school board meeting?"
- "What's the district's attendance policy?"
- "How do I apply to be a substitute teacher?"
- "What are the graduation requirements?"

## Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4o, LangChain
- **Web Crawling**: Firecrawl AI
- **Vector Database**: ChromaDB
- **PDF Processing**: Unstructured

## How It Works

1. **Data Ingestion**: Firecrawl crawls argyleisd.com and loads PDF documents
2. **Embedding**: Content is converted to vector embeddings using OpenAI
3. **Storage**: Embeddings are stored in ChromaDB for fast retrieval
4. **Query Processing**: User questions are matched against the knowledge base
5. **Response Generation**: GPT-4o generates answers with source citations

## Configuration

### PDF Documents

The app includes these PDF documents by default:

- 2024-2025 School Calendar
- Student Handbook

To add more PDFs, update the `pdf_urls` list in `app.py`:

```python
pdf_urls = [
    "https://www.argyleisd.com/path/to/your/document.pdf",
    # Add more URLs here
]
```

### Crawling Depth

Adjust the crawling depth in `app.py`:

```python
params={"maxDepth": 2, "formats": ["markdown"]}
```

## Deployment

For production deployment:

1. Use environment variables for API keys
2. Consider using a persistent vector database
3. Add rate limiting for public access
4. Monitor usage and costs

## Contributing

This is a community project for Argyle ISD. Contributions welcome!

## License

MIT License - Built with ❤️ for the Argyle ISD community
