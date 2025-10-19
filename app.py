import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import os
from datetime import datetime


# Page config must be first Streamlit command
st.set_page_config(
    page_title="Wake Forest Document Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules directly
from drive_handler import DriveHandler
from rag_engine import RAGEngine
from supabase_store import SupabaseVectorStore

# Load custom CSS for Wake Forest branding
def load_css():
    st.markdown("""
    <style>
    /* Wake Forest Color Scheme */
    :root {
        --wfu-gold: #9E7E38;
        --wfu-black: #000000;
        --wfu-white: #FFFFFF;
    }
    
    /* Main app styling */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Force all text to be black */
    .stApp * {
        color: #000000 !important;
    }
    
    /* Specific text elements */
    p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Header styling - more prominent */
    .main-header {
        background-color: var(--wfu-black) !important;
        padding: 1.5rem !important;
        border-radius: 10px !important;
        margin: 2rem 0 !important;
        text-align: center !important;
        width: 100% !important;
        max-width: 800px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    .main-header h1 {
        color: var(--wfu-gold) !important;
        margin: 0 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    .main-header p {
        color: var(--wfu-white) !important;
        margin: 0.5rem 0 0 0 !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--wfu-gold) !important;
        color: var(--wfu-black) !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        background-color: #B8954A !important;
        color: var(--wfu-black) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
    }
    
    /* Main content area - more aggressive styling */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Fix column spacing and center content */
    [data-testid="column"] {
        padding: 0.5rem !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    /* Center the main content and fix width issues */
    .main {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Force proper layout */
    .stApp > div:first-child {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
    }
    
    /* Fix the main content container */
    section.main > div:first-child {
        width: 100% !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 2rem 1rem !important;
    }
    
    /* Responsive adjustments */
    @media (min-width: 768px) {
        .main .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        section.main > div:first-child {
            padding: 2rem !important;
        }
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #F9F9F9;
        border-left: 4px solid var(--wfu-gold);
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border: 2px solid #CCCCCC !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--wfu-gold) !important;
        box-shadow: 0 0 0 0.1rem rgba(158, 126, 56, 0.25) !important;
    }
    
    /* Fix text area styling */
    .stTextArea>div>div>textarea {
        border: 2px solid #CCCCCC !important;
        border-radius: 5px !important;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: var(--wfu-gold) !important;
        box-shadow: 0 0 0 0.1rem rgba(158, 126, 56, 0.25) !important;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: #E8F5E9;
        border-left: 4px solid var(--wfu-gold);
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: #FFF3E0;
        border-left: 4px solid var(--wfu-gold);
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem 0;
    }
    
    /* Source citation styling */
    .source-box {
        background-color: #F5F5F5;
        border: 1px solid #DDDDDD;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .source-title {
        color: var(--wfu-gold);
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #666666;
        font-size: 0.85rem;
        border-top: 1px solid #EEEEEE;
        margin-top: 3rem;
    }
    
    /* Logo container centering */
    .logo-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-bottom: 1rem !important;
    }
    
    /* Fix any remaining layout issues */
    div[data-testid="stVerticalBlock"] > div:first-child {
        width: 100% !important;
    }
    
    /* Ensure sidebar doesn't overlap */
    @media (max-width: 768px) {
        .main {
            margin-left: 0 !important;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'indexed' not in st.session_state:
        st.session_state.indexed = False
    if 'indexing' not in st.session_state:
        st.session_state.indexing = False

# Load authentication configuration
def load_auth_config():
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Main app function
def main():
    load_css()
    init_session_state()
    
    # Load authentication
    config = load_auth_config()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    # Login widget
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    if authentication_status == False:
        st.error('Username/password is incorrect')
        return
    
    if authentication_status == None:
        st.warning('Please enter your username and password')
        return
    
    # User is authenticated
    if authentication_status:
        # Display logo and header
        # Center the logo and header
        logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
        with logo_col2:
            logo_path = Path(__file__).parent / 'assets' / 'WFU_Univ_Shield_Black.png'
            if logo_path.exists():
                st.image(str(logo_path), width=120)
        
        st.markdown("""
        <div class="main-header">
            <h1>Wake Forest Document Assistant</h1>
            <p>Intelligent Document Search & Retrieval System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"### Welcome, {name}!")
            authenticator.logout('Logout', 'sidebar')
            
            st.markdown("---")
            st.markdown("### System Status")
            
            if st.session_state.indexed:
                st.success("✓ Documents Indexed")
            else:
                st.warning("⚠ Documents Not Indexed")
            
            st.markdown("---")
            st.markdown("### Settings")
            
            # Index documents section
            with st.expander("📁 Index Documents", expanded=not st.session_state.indexed):
                st.markdown("**Google Drive Folder ID:**")
                st.caption("Find this in your folder's URL after 'folders/'")
                folder_id = st.text_input("Folder ID", key="folder_id", label_visibility="collapsed")
                
                if st.button("Index Documents", disabled=st.session_state.indexing):
                    if folder_id:
                        index_documents(folder_id)
                    else:
                        st.error("Please enter a folder ID")
            
            # Clear conversation
            if st.button("🗑️ Clear Conversation"):
                st.session_state.messages = []
                st.rerun()
            
            # System info
            st.markdown("---")
            st.markdown("### About")
            st.caption("Powered by Claude AI")
            st.caption("Vector Storage: Supabase")
            st.caption("© 2025 Wake Forest University")
        
        # Main chat interface
        if st.session_state.indexed:
            display_chat_interface()
        else:
            display_welcome_message()
        
        # Footer
        st.markdown("""
        <div class="footer">
            <p>Wake Forest University Document Assistant | Secure & Private</p>
        </div>
        """, unsafe_allow_html=True)

def display_welcome_message():
    st.markdown("""
    ### Getting Started
    
    Welcome to the Wake Forest Document Assistant! This system allows you to search and query 
    documents from your Google Drive using natural language.
    
    **To begin:**
    1. Click on "Index Documents" in the sidebar
    2. Enter your Google Drive folder ID
    3. Click "Index Documents" to process your files
    4. Start asking questions about your documents!
    
    **Features:**
    - 🔍 Semantic search across all document types
    - 📄 Support for PDFs, DOCX, XLSX, TXT, and more
    - 🔒 Secure and private - your data stays in your control
    - 💬 Natural language queries powered by Claude AI
    - 📚 Source citations for all answers
    """)

def display_chat_interface():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        <div class="source-box">
                            <div class="source-title">Source {i}: {source['title']}</div>
                            <div style="font-size: 0.85rem; color: #666; margin-top: 0.3rem;">
                                {source['snippet']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating response..."):
                response, sources = get_ai_response(prompt)
                st.markdown(response)
                
                if sources:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"""
                            <div class="source-box">
                                <div class="source-title">Source {i}: {source['title']}</div>
                                <div style="font-size: 0.85rem; color: #666; margin-top: 0.3rem;">
                                    {source['snippet']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "sources": sources
        })

def index_documents(folder_id):
    st.session_state.indexing = True
    
    try:
        with st.spinner("Initializing..."):
            # Initialize components
            drive_handler = DriveHandler()
            vector_store = SupabaseVectorStore()
            
            st.info("📂 Scanning Google Drive folder...")
        
        # Get all files recursively
        with st.spinner("Scanning folders..."):
            files = drive_handler.get_all_files_recursive(folder_id)
            st.success(f"Found {len(files)} files")
        
        # Process and index files
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        indexed_count = 0
        for i, file_info in enumerate(files):
            try:
                status_text.text(f"Processing: {file_info['name']}")
                
                # Extract text content
                content = drive_handler.extract_content(file_info)
                
                if content:
                    # Create chunks and embeddings
                    chunks = vector_store.create_chunks(content, file_info)
                    vector_store.add_documents(chunks)
                    indexed_count += 1
                
                progress_bar.progress((i + 1) / len(files))
            except Exception as e:
                st.warning(f"Skipped {file_info['name']}: {str(e)}")
        
        # Initialize RAG engine
        st.session_state.rag_engine = RAGEngine(vector_store)
        st.session_state.indexed = True
        
        status_text.empty()
        progress_bar.empty()
        st.success(f"✓ Successfully indexed {indexed_count} documents!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error during indexing: {str(e)}")
        st.error("Please check your credentials and folder ID.")
    
    finally:
        st.session_state.indexing = False

def get_ai_response(query):
    """Get response from RAG engine"""
    try:
        if st.session_state.rag_engine:
            response, sources = st.session_state.rag_engine.query(query)
            return response, sources
        else:
            return "RAG engine not initialized. Please index documents first.", []
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I encountered an error processing your query. Please try again.", []

if __name__ == "__main__":
    main()
