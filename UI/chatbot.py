import streamlit as st
import streamlit.components.v1 as components
import requests
import uuid
import re
import time
import json
from datetime import datetime

# Page configuration with custom styling
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

/* Main container styling */
.main .block-container {
    padding: 2rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Title styling */
.main-title {
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 0 0 30px rgba(79, 172, 254, 0.3);
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    border-radius: 15px;
    margin: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* Chat container */
.chat-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

/* Message bubbles */
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px 20px 5px 20px;
    padding: 15px 20px;
    margin: 10px 0;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    animation: slideInRight 0.5s ease-out;
    display: block;
    width: 100%;
}

.bot-message {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border-radius: 20px 20px 20px 5px;
    padding: 15px 20px;
    margin: 10px 0;
    box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    animation: slideInLeft 0.5s ease-out;
    display: block;
    width: 100%;
}

.bot-message * {
    color: white !important;
}

.bot-message p {
    margin: 0.5em 0 !important;
    color: white !important;
}

.bot-message h1, .bot-message h2, .bot-message h3, .bot-message h4, .bot-message h5, .bot-message h6 {
    color: white !important;
    margin: 1em 0 0.5em 0 !important;
}

.bot-message code {
    background: rgba(0, 0, 0, 0.2) !important;
    color: #fff !important;
    padding: 2px 4px !important;
    border-radius: 4px !important;
}

.bot-message pre {
    background: rgba(0, 0, 0, 0.2) !important;
    color: #fff !important;
    padding: 10px !important;
    border-radius: 8px !important;
    overflow-x: auto !important;
}

.bot-message ul, .bot-message ol {
    color: white !important;
    padding-left: 1.5em !important;
}

.bot-message li {
    color: white !important;
    margin: 0.25em 0 !important;
}

.bot-message blockquote {
    border-left: 4px solid rgba(255, 255, 255, 0.3) !important;
    padding-left: 1em !important;
    margin: 1em 0 !important;
    color: white !important;
    font-style: italic;
}

/* Animations */
@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Loading animation */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 15px 20px;
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    border-radius: 20px 20px 20px 5px;
    margin: 10px 0;
    animation: pulse 2s infinite;
}

.typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: white;
    animation: typingDots 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typingDots {
    0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Input styling */
.stChatInput input {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 25px;
    color: white;
    padding: 15px 20px;
    font-size: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stChatInput input:focus {
    border-color: #4facfe;
    box-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
    outline: none;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Source cards */
.source-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.source-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Sidebar elements */
.sidebar-section {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Metrics styling */
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    margin: 10px 0;
}

/* Expandable content */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: white;
    font-weight: 600;
}

/* JSON viewer */
.stJson {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Status indicators */
.status-online {
    color: #2ecc71;
    font-weight: 600;
}

.status-error {
    color: #e74c3c;
    font-weight: 600;
}

/* Floating elements */
.floating-stats {
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/query"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

headers = {
    "Content-Type": "application/json",
    "email": "mansoor.b@digitalapicraft.com",
    "session_id": st.session_state.session_id,
}


def render_markdown_with_html(content):
    """Render markdown content that may contain HTML tags."""
    if not content:
        return

    html_pattern = r'<[^>]+>'
    has_html = bool(re.search(html_pattern, content))

    if has_html:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.markdown(content)


def create_expandable_content(content, max_length=500):
    """Create expandable content for long responses."""
    if len(content) <= max_length:
        return render_markdown_with_html(content)

    preview = content[:max_length] + "..."

    with st.expander("📄 Show Full Response", expanded=False):
        render_markdown_with_html(content)

    st.markdown("**Preview:**")
    render_markdown_with_html(preview)


def render_typing_animation():
    """Render a beautiful typing animation."""
    st.markdown("""
    <div class="typing-indicator">
        <span style="margin-right: 10px;">🤖 AI is thinking</span>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)


def render_bot_message(content):
    """Render bot message with proper styling."""
    st.markdown(f"""
    <div class="bot-message">
        🤖 {content}
    </div>
    """, unsafe_allow_html=True)


# Main title with animation
st.markdown('<h1 class="main-title">🤖 AI Assistant Pro</h1>', unsafe_allow_html=True)

# Floating stats
session_duration = datetime.now() - st.session_state.start_time
st.markdown(f"""
<div class="floating-stats">
    <div style="font-size: 12px; color: rgba(255,255,255,0.8);">Session Stats</div>
    <div style="font-size: 14px; font-weight: 600; color: white;">
        💬 {st.session_state.message_count} messages<br>
        ⏱️ {str(session_duration).split('.')[0]}
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 Session Control")

    # Session info with better styling
    st.markdown(f"""
    <div class="metric-card">
        <h4>Session ID</h4>
        <code>{st.session_state.session_id[:8]}...</code>
    </div>
    """, unsafe_allow_html=True)

    # Connection status
    try:
        test_response = requests.get("http://127.0.0.1:8000/", timeout=2)
        status = "🟢 Online" if test_response.status_code == 200 else "🟡 Issues"
        status_class = "status-online"
    except:
        status = "🔴 Offline"
        status_class = "status-error"

    st.markdown(f'<div class="{status_class}">API Status: {status}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Debug section with modern styling
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 Debug Console")

    if "debug_info" not in st.session_state:
        st.session_state.debug_info = {
            "last_payload": None,
            "last_response": None,
            "last_error": None,
            "api_url": API_URL,
            "headers": headers
        }

    # Show API configuration
    with st.expander("⚙️ API Configuration", expanded=False):
        st.json({
            "api_url": st.session_state.debug_info["api_url"],
            "headers": st.session_state.debug_info["headers"]
        })

    # Show last payload
    if st.session_state.debug_info["last_payload"]:
        with st.expander("📤 Last Request", expanded=False):
            st.json(st.session_state.debug_info["last_payload"])

    # Show last response
    if st.session_state.debug_info["last_response"]:
        with st.expander("📥 Last Response", expanded=False):
            st.json(st.session_state.debug_info["last_response"])

    # Show last error if any
    if st.session_state.debug_info["last_error"]:
        with st.expander("⚠️ Last Error", expanded=True):
            st.error(st.session_state.debug_info["last_error"])

    # Clear debug info button
    if st.button("🗑️ Clear Debug", key="clear_debug"):
        st.session_state.debug_info = {
            "last_payload": None,
            "last_response": None,
            "last_error": None,
            "api_url": API_URL,
            "headers": headers
        }
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Display settings
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Display Settings")

    enable_html = st.checkbox("🔧 Enable HTML Rendering", value=True,
                              help="Allow HTML tags in bot responses")

    max_preview_length = st.slider("📏 Preview Length",
                                   min_value=200, max_value=1000, value=500,
                                   help="Maximum characters to show before expandable section")

    show_sources = st.checkbox("📚 Show Sources", value=True,
                               help="Display source information in responses")

    auto_scroll = st.checkbox("📜 Auto Scroll", value=True,
                              help="Automatically scroll to new messages")

    # Store settings in session state
    st.session_state.enable_html = enable_html
    st.session_state.max_preview_length = max_preview_length
    st.session_state.show_sources = show_sources
    st.session_state.auto_scroll = auto_scroll
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick actions
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", key="new_chat"):
            st.session_state.chat_history = []
            st.session_state.message_count = 0
            st.session_state.start_time = datetime.now()
            st.rerun()

    with col2:
        if st.button("💾 Export", key="export_chat"):
            if "chat_history" in st.session_state:
                chat_data = {
                    "session_id": st.session_state.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.chat_history
                }
                st.download_button(
                    "📥 Download JSON",
                    data=json.dumps(chat_data, indent=2),
                    file_name=f"chat_export_{st.session_state.session_id[:8]}.json",
                    mime="application/json"
                )
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input with enhanced styling
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

user_input = st.chat_input("💭 Ask me anything... I'm here to help!")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", "loading"))
    st.session_state.message_count += 1

# Check if we need to process the last message
if (st.session_state.chat_history and
        st.session_state.chat_history[-1][0] == "Bot" and
        st.session_state.chat_history[-1][1] == "loading"):

    # Display chat history first (including the loading state)
    for sender, message in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            if sender == "You":
                st.markdown(f'<div class="user-message">👤 {message}</div>', unsafe_allow_html=True)
            elif sender == "Bot" and message == "loading":
                render_typing_animation()

    # Now make the API call
    user_message = st.session_state.chat_history[-2][1]

    payload = {"message": user_message, "consent": True}

    # Store payload in debug info
    st.session_state.debug_info["last_payload"] = payload
    st.session_state.debug_info["last_error"] = None

    try:
        with st.spinner("🔮 Processing your request..."):
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            bot_reply = response.json()
            bot_message = bot_reply.get("message", "")
            bot_sources = bot_reply.get("sources", [])

            # Store response in debug info
            st.session_state.debug_info["last_response"] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": bot_reply
            }

    except Exception as e:
        bot_message = f"❌ Oops! Something went wrong: {str(e)}"
        st.session_state.debug_info["last_error"] = str(e)
        st.session_state.debug_info["last_response"] = None
        bot_sources = []

    # Replace loading message with actual response
    st.session_state.chat_history[-1] = ("Bot", {"message": bot_message, "sources": bot_sources})
    st.rerun()

else:
    # Display chat history normally when not loading
    for i, (sender, message) in enumerate(st.session_state.chat_history):
        with st.chat_message("user" if sender == "You" else "assistant"):
            if sender == "You":
                st.markdown(f'<div class="user-message">👤 {message}</div>', unsafe_allow_html=True)
            else:
                # Handle bot responses that might have sources
                if isinstance(message, dict):
                    # Extract message and sources from dictionary
                    if "message" in message:
                        bot_message = message["message"]
                        bot_sources = message.get("sources", [])

                        if bot_sources and st.session_state.get("show_sources", True):
                            # Create tabs for message and sources
                            tab1, tab2 = st.tabs(["💬 Response", "📚 Sources"])

                            with tab1:
                                render_bot_message(bot_message)

                            with tab2:
                                st.markdown("### 📚 Source References")
                                for j, source in enumerate(bot_sources, 1):
                                    st.markdown(f"""
                                    <div class="source-card">
                                        <h4>🔗 Source {j}: {source.get('source_name', 'Unknown Source')}</h4>
                                    """, unsafe_allow_html=True)

                                    if source.get('content_type'):
                                        st.markdown(f"**Type:** `{source.get('content_type')}`")

                                    if source.get('source_url'):
                                        url = source['source_url']
                                        st.markdown(f"**URL:** [🌐 {url}]({url})")

                                    if source.get('data'):
                                        with st.expander(f"📊 View Data for Source {j}", expanded=False):
                                            try:
                                                if isinstance(source['data'], str):
                                                    if source['data'].strip().startswith(('{', '[')):
                                                        parsed_data = json.loads(source['data'])
                                                        st.json(parsed_data)
                                                    else:
                                                        st.code(source['data'], language='text')
                                                else:
                                                    st.json(source['data'])
                                            except json.JSONDecodeError:
                                                st.code(source['data'], language='text')
                                            except Exception:
                                                st.text(str(source['data']))

                                    st.markdown("</div>", unsafe_allow_html=True)

                                    if j < len(bot_sources):
                                        st.markdown("---")
                        else:
                            # No sources or sources disabled - show message directly
                            render_bot_message(bot_message)
                    else:
                        # Dictionary without 'message' key - show as string
                        render_bot_message(str(message))
                else:
                    # Handle simple string messages (backward compatibility)
                    render_bot_message(message)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll to bottom if enabled
if st.session_state.get("auto_scroll", True) and st.session_state.chat_history:
    st.markdown("""
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """, unsafe_allow_html=True)

# Welcome message for new users
if not st.session_state.chat_history:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.8);">
        <h3>👋 Welcome to AI Assistant Pro!</h3>
        <p>I'm here to help you with any questions or tasks. Just type your message below to get started!</p>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">💡 Ask questions</span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">🔍 Get research help</span>
            <span style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">💬 Have conversations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
