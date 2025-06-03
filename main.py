import streamlit as st
import os
from pathlib import Path
from document_processor import DocumentProcessor
from summarizer import Summarizer
from rag_qa import RAGQA
from conversation import ConversationalAgent
from config import Config
import time
import base64
from streamlit.components.v1 import html
import random

# Sophisticated CSS with professional dark theme
def load_css():
    st.markdown("""
    <style>
        /* Professional dark theme */
        :root {
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --secondary: #7c3aed;
            --accent: #4f46e5;
            --dark: #0f172a;
            --darker: #020617;
            --light: #1e293b;
            --text: #e2e8f0;
            --text-light: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --error: #ef4444;
            --warning: #f59e0b;
            --border: #1e293b;
        }
        
        /* Main app styling */
        .stApp {
            background-color: var(--dark);
            color: var(--text);
            min-height: 100vh;
        }
        
        /* Elegant title styling */
        .title-container {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .title-container h1 {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--text-light);
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }
        
        .title-container p {
            color: var(--text-muted);
            max-width: 800px;
            margin: 0 auto;
            font-size: 1.1rem;
        }
        
        /* Subtle divider */
        .divider {
            height: 1px;
            width: 120px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            margin: 1rem auto;
            opacity: 0.5;
        }
        
        /* Professional cards */
        .card {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(8px);
            padding: 1.75rem;
            margin-bottom: 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card:hover {
            border-color: var(--primary);
            box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.25rem;
        }
        
        .card-icon {
            font-size: 1.75rem;
            margin-right: 1rem;
            color: var(--primary);
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-light);
            margin: 0;
        }
        
        .card-subtitle {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin: 0;
        }
        
        /* Professional buttons */
        .stButton>button {
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            background: var(--primary);
            color: white;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stButton>button:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Secondary button */
        .stButton>button[kind="secondary"] {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text);
        }
        
        .stButton>button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--primary);
            color: var(--text-light);
        }
        
        /* Tabs with professional style */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.25rem;
            margin: 0;
            color: var(--text-muted);
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-light);
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(37, 99, 235, 0.2);
            color: var(--primary);
        }
        
        /* Chat messages */
        .stChatMessage {
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
            max-width: 85%;
            border: 1px solid var(--border);
        }
        
        [data-testid="stChatMessage-user"] {
            background: rgba(37, 99, 235, 0.1);
            border-color: rgba(37, 99, 235, 0.3);
            margin-left: auto;
        }
        
        [data-testid="stChatMessage-assistant"] {
            background: rgba(15, 23, 42, 0.7);
            border-color: var(--border);
            margin-right: auto;
        }
        
        /* Input fields */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border);
            color: var(--text-light);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus, 
        .stTextArea>div>div>textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
            background: rgba(15, 23, 42, 0.9);
        }
        
        /* File uploader */
        .stFileUploader {
            border: 1px dashed var(--border);
            border-radius: 12px;
            padding: 2rem;
            background: rgba(15, 23, 42, 0.3);
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: var(--primary);
            background: rgba(15, 23, 42, 0.5);
        }
        
        /* Progress spinner */
        .stSpinner>div>div {
            border: 3px solid rgba(37, 99, 235, 0.2);
            border-top: 3px solid var(--primary);
        }
        
        /* Status messages */
        .stAlert {
            border-left: 4px solid;
            border-radius: 8px;
        }
        
        .stAlert[data-status="success"] {
            background: rgba(16, 185, 129, 0.1);
            border-color: var(--success);
        }
        
        .stAlert[data-status="error"] {
            background: rgba(239, 68, 68, 0.1);
            border-color: var(--error);
        }
        
        .stAlert[data-status="warning"] {
            background: rgba(245, 158, 11, 0.1);
            border-color: var(--warning);
        }
        
        .stAlert[data-status="info"] {
            background: rgba(37, 99, 235, 0.1);
            border-color: var(--primary);
        }
        
        /* Floating animation */
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .title-container h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 1.25rem;
            }
        }
        
        /* Smooth transitions */
        * {
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 3px;
        }
        
        /* Animated background elements */
        .bg-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.03;
            background-image: radial-gradient(var(--primary) 1px, transparent 1px);
            background-size: 20px 20px;
            animation: move 120s linear infinite;
        }
        
        @keyframes move {
            0% { background-position: 0 0; }
            100% { background-position: 1000px 1000px; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add subtle background pattern
    st.markdown('<div class="bg-pattern"></div>', unsafe_allow_html=True)

# Initialize UI with professional design
load_css()

# Initialize directories and session state
Config.create_directories()

if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# Professional app header
st.markdown("""
<div class="title-container">
    <h1>Domain Knowledge AI</h1>
    <div class="divider"></div>
    <p>
        Advanced document processing with semantic analysis and contextual understanding
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">📊</div>
            <div>
                <h3 class="card-title">Semantic Analysis</h3>
                <p class="card-subtitle">Deep understanding of document content</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">🔍</div>
            <div>
                <h3 class="card-title">Contextual Search</h3>
                <p class="card-subtitle">Find relevant information across documents</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">📝</div>
            <div>
                <h3 class="card-title">Intelligent Summarization</h3>
                <p class="card-subtitle">Concise overviews of complex documents</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">💬</div>
            <div>
                <h3 class="card-title">Conversational Interface</h3>
                <p class="card-subtitle">Natural language interaction with your data</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with professional styling
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: var(--text-light); margin-bottom: 0.5rem;">Document Processing</h2>
        <div class="divider" style="margin: 0.5rem 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "docx", "pptx", "md"],
        accept_multiple_files=True,
        help="Supported formats: PDF, TXT, DOCX, PPTX, MD"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        process_btn = st.button("Process", 
                              help="Process uploaded documents",
                              use_container_width=True)
    with col2:
        clear_btn = st.button("Reset", 
                            help="Clear all processed data",
                            type="secondary",
                            use_container_width=True)
    
    if clear_btn:
        processor = DocumentProcessor()
        if processor.clear_data():
            st.session_state.vector_store = None
            st.session_state.processed_files = set()
            st.session_state.chat_history = []
            st.success("Processing cache cleared", icon="✅")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Reset failed", icon="❌")
    
    if st.session_state.processed_files:
        st.markdown("""
        <div style="margin-top: 1.5rem;">
            <h3 style="color: var(--text-light); margin-bottom: 0.5rem;">Processed Files</h3>
            <div class="divider" style="margin: 0.5rem 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        for file in st.session_state.processed_files:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem; padding: 0.75rem; 
                        background: rgba(30, 41, 59, 0.5); border-radius: 8px;
                        border-left: 3px solid var(--success);">
                <span style="color: var(--success); margin-right: 0.75rem;">✓</span>
                <span style="color: var(--text); flex-grow: 1; font-size: 0.9rem;">{file}</span>
            </div>
            """, unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3 = st.tabs(["Summarization", "Q&A", "Conversation"])

# Document processing
if process_btn and uploaded_files:
    with st.spinner("Processing documents..."):
        processor = DocumentProcessor()
        success_count = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                if uploaded_file.name in st.session_state.processed_files:
                    continue
                
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing {uploaded_file.name}...")
                
                upload_path = Path(Config.UPLOAD_FOLDER) / uploaded_file.name
                with open(upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                processor.process_document(str(upload_path))
                st.session_state.processed_files.add(uploaded_file.name)
                success_count += 1
                
                os.remove(upload_path)
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        
        progress_bar.empty()
        status_text.empty()
        
        if success_count > 0:
            st.session_state.vector_store = processor.get_vector_store()
            st.success(f"Processed {success_count} document(s)", icon="✅")
            time.sleep(1)
            st.rerun()

# Summarization Tab
with tab1:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">📝</div>
            <div>
                <h3 class="card-title">Document Summarization</h3>
                <p class="card-subtitle">Generate concise summaries from text or documents</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    summary_option = st.radio(
        "Summary source:",
        ["Enter text", "From processed documents"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if summary_option == "Enter text":
        summary_text = st.text_area(
            "Text to summarize",
            height=200,
            placeholder="Enter text to summarize...",
            label_visibility="collapsed"
        )
    else:
        if not st.session_state.vector_store:
            st.warning("No documents processed - upload and process files first", icon="⚠️")
            summary_text = ""
        else:
            docs = st.session_state.vector_store.similarity_search("", k=100)
            summary_text = "\n\n".join([doc.page_content for doc in docs])
            st.info(f"Analyzing content from {len(docs)} document chunks", icon="🔍")
    
    if st.button("Generate Summary", key="summary-btn", use_container_width=True) and summary_text:
        with st.spinner("Generating summary..."):
            summarizer = Summarizer()
            try:
                summary = summarizer.summarize(summary_text)
                
                st.markdown("""
                <div style="margin-top: 1.5rem; background: rgba(30, 41, 59, 0.5); 
                            padding: 1.5rem; border-radius: 12px; 
                            border-left: 3px solid var(--primary);">
                    <h3 style="color: var(--text-light); margin-top: 0;">Summary</h3>
                    <div style="color: var(--text); line-height: 1.6;">
                """, unsafe_allow_html=True)
                
                summary_placeholder = st.empty()
                full_summary = ""
                for word in summary.split():
                    full_summary += word + " "
                    time.sleep(0.02)
                    summary_placeholder.markdown(f"""
                    <div style="color: var(--text); line-height: 1.6;">
                        {full_summary}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Summarization failed: {str(e)}", icon="❌")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Q&A Tab
with tab2:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">🔍</div>
            <div>
                <h3 class="card-title">Document Q&A</h3>
                <p class="card-subtitle">Ask questions about your processed documents</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.vector_store:
        st.warning("No documents processed - process documents first", icon="⚠️")
    else:
        question = st.text_input(
            "Your question",
            placeholder="Ask a question about the documents...",
            label_visibility="collapsed"
        )
        
        if st.button("Submit Question", key="qa-btn", use_container_width=True) and question:
            retriever = st.session_state.vector_store.as_retriever()
            qa = RAGQA(retriever)
            
            with st.spinner("Analyzing documents..."):
                try:
                    answer = qa.answer_question(question)
                    
                    st.markdown("""
                    <div style="margin-top: 1.5rem; background: rgba(30, 41, 59, 0.5); 
                                padding: 1.5rem; border-radius: 12px; 
                                border-left: 3px solid var(--primary);">
                        <h3 style="color: var(--text-light); margin-top: 0;">Answer</h3>
                        <div style="color: var(--text); line-height: 1.6;">
                    """, unsafe_allow_html=True)
                    
                    answer_placeholder = st.empty()
                    full_answer = ""
                    for word in answer.split():
                        full_answer += word + " "
                        time.sleep(0.02)
                        answer_placeholder.markdown(f"""
                        <div style="color: var(--text); line-height: 1.6;">
                            {full_answer}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append((question, answer))
                except Exception as e:
                    st.error(f"Failed to answer question: {str(e)}", icon="❌")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Conversation Tab
with tab3:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">💬</div>
            <div>
                <h3 class="card-title">Conversation</h3>
                <p class="card-subtitle">Interactive chat with your documents</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.conversation is None:
        st.session_state.conversation = ConversationalAgent()
    
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"""
            <div style="font-weight: 500; color: var(--text-light);">
                {question}
            </div>
            """, unsafe_allow_html=True)
            
        with st.chat_message("assistant"):
            st.markdown(f"""
            <div style="color: var(--text);">
                {answer}
            </div>
            """, unsafe_allow_html=True)
    
    if prompt := st.chat_input("Type your message..."):
        with st.chat_message("user"):
            st.markdown(f"""
            <div style="font-weight: 500; color: var(--text-light);">
                {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.conversation.chat(prompt)
                    
                    response_placeholder = st.empty()
                    full_response = ""
                    for word in response.split():
                        full_response += word + " "
                        time.sleep(0.03)
                        response_placeholder.markdown(f"""
                        <div style="color: var(--text); line-height: 1.6;">
                            {full_response}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append((prompt, response))
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}", icon="❌")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Add subtle interactive effects
html("""
<script>
// Smooth hover effects
document.querySelectorAll('.card, .stButton>button').forEach(el => {
    el.addEventListener('mouseenter', () => {
        el.style.transform = 'translateY(-2px)';
    });
    
    el.addEventListener('mouseleave', () => {
        el.style.transform = '';
    });
});

// Auto-scroll chat
function scrollToBottom() {
    const chatContainer = document.querySelector('[data-testid="stVerticalBlock"]:last-child');
    if (chatContainer) {
        chatContainer.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
}

// Scroll on new message
const observer = new MutationObserver(scrollToBottom);
const chatContainer = document.querySelector('[data-testid="stVerticalBlock"]:last-child');
if (chatContainer) {
    observer.observe(chatContainer, { childList: true, subtree: true });
}

// Input field focus effects
document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('focus', () => {
        input.style.boxShadow = '0 0 0 2px rgba(37, 99, 235, 0.3)';
    });
    
    input.addEventListener('blur', () => {
        input.style.boxShadow = '';
    });
});
</script>
""")