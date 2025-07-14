# �� Argyle ISD AI App: Real Data Version

import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any
import re

# LangChain imports (updated to avoid deprecation warnings)
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

# ---- STEP 1: Set Your API Keys ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ---- STEP 2: Web Scraping Functions ----


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    return text.strip()


def scrape_url(url: str) -> Dict[str, Any]:
    """Scrape a single URL and return structured data."""
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36')
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text() if title else "No Title"
        
        # Extract main content
        content = soup.get_text()
        content = clean_text(content)
        
        return {
            "url": url,
            "title": title_text,
            "content": content[:5000]  # Limit content length
        }
    except Exception as e:
        st.warning(f"Failed to scrape {url}: {str(e)}")
        return None

def get_argyle_urls() -> List[str]:
    """Get list of important Argyle ISD URLs to scrape."""
    return [
        "https://www.argyleisd.com/",
        "https://www.argyleisd.com/about",
        "https://www.argyleisd.com/board-of-trustees",
        "https://www.argyleisd.com/schools",
        "https://www.argyleisd.com/departments",
        "https://www.argyleisd.com/calendars",
        "https://www.argyleisd.com/employment",
        "https://www.argyleisd.com/departments/transportation",
        "https://www.argyleisd.com/departments/human-resources",
        "https://www.argyleisd.com/all-news",
        "https://www.argyleisd.com/about/faqs",
        "https://www.argyleisd.com/future/bonds",
        "https://www.argyleisd.com/staff",
        "https://www.argyleisd.com/directory"
    ]

@st.cache_data
def load_argyle_data() -> List[Document]:
    """Load real data from Argyle ISD website."""
    st.info("🌐 Loading real data from Argyle ISD website...")
    
    urls = get_argyle_urls()
    docs = []
    
    progress_bar = st.progress(0)
    for i, url in enumerate(urls):
        st.text(f"📥 Scraping: {url}")
        
        data = scrape_url(url)
        if data and data["content"]:
            # Create document
            doc = Document(
                page_content=data["content"],
                metadata={
                    "source": data["url"],
                    "title": data["title"]
                }
            )
            docs.append(doc)
        
        progress_bar.progress((i + 1) / len(urls))
        time.sleep(0.5)  # Be respectful to the server
    
    st.success(f"✅ Successfully loaded {len(docs)} documents from Argyle ISD")
    return docs

@st.cache_resource
def get_vectorstore() -> Chroma:
    """Create or load the vector store."""
    st.info("🧠 Creating knowledge base...")
    
    # Load documents
    docs = load_argyle_data()
    
    if not docs:
        st.error("❌ No documents loaded! Please check the network connection.")
        return None
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Create vector store with persistent storage
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="argyleisd_real",
        persist_directory="./chroma_db_real"
    )
    
    st.success("✅ Knowledge base created successfully!")
    return vectorstore

@st.cache_resource
def get_qa_chain(_vectorstore):
    """Create the QA chain."""
    if not _vectorstore:
        return None
        
    llm = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.1,
        max_tokens=500
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=_vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    
    return qa_chain

# ---- STEP 3: Streamlit UI ----

def main():
    # Page config
    st.set_page_config(
        page_title="Argyle ISD AI Guide",
        page_icon="🎓",
        layout="wide"
    )
    
    # Header
    st.title("🎓 Argyle ISD AI Guide")
    st.markdown("### Ask any question about Argyle Independent School District")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Status")
        
        if os.path.exists("./chroma_db_real"):
            st.success("💾 Database: Ready")
        else:
            st.info("💾 Database: Building...")
        
        if OPENAI_API_KEY:
            st.success("🔑 OpenAI: Connected")
        else:
            st.error("🔑 OpenAI: Not configured")
        
        # Clear cache button
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    
    # Initialize system
    try:
        vectorstore = get_vectorstore()
        if not vectorstore:
            st.error("❌ Failed to initialize the knowledge base. Please check your network connection.")
            return
            
        qa_chain = get_qa_chain(vectorstore)
        if not qa_chain:
            st.error("❌ Failed to initialize the QA system.")
            return
            
        # Store in session state
        st.session_state.qa_chain = qa_chain
        st.session_state.vectorstore = vectorstore
        
    except Exception as e:
        st.error(f"❌ System initialization failed: {str(e)}")
        return
    
    # Main interface
    st.markdown("### 💬 Ask your question:")
    
    # Question input
    user_question = st.text_input(
        "Enter your question about Argyle ISD:",
        placeholder="e.g., 'Who is on the board of trustees?'"
    )
    
    if user_question:
        with st.spinner("🔍 Searching for information..."):
            try:
                result = st.session_state.qa_chain.invoke({"query": user_question})
                
                # Display answer
                st.markdown("### 📝 Answer:")
                st.write(result["result"])
                
                # Display sources
                if "source_documents" in result and result["source_documents"]:
                    st.markdown("### 📚 Sources:")
                    for i, doc in enumerate(result["source_documents"][:3]):
                        source_url = doc.metadata.get("source", "Unknown")
                        st.markdown(f"**{i+1}.** [{source_url}]({source_url})")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Please try rephrasing your question or check your API keys.")

if __name__ == "__main__":
    main() 