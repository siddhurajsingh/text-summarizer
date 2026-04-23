import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* General styling */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
    }
    
    /* Cards styling */
    .stContainer {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Metric styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #6366f1;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
        border-radius: 10px 10px 0 0;
    }
    
    /* Alert boxes */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
    }
    
    .stWarning {
        background-color: #fef3c7 !important;
        border-left: 4px solid #f59e0b !important;
    }
    
    .stError {
        background-color: #fee2e2 !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    /* Info box */
    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        padding: 0.75rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child > div:first-child {
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 2px solid #e2e8f0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: #e0e7ff;
        color: #4f46e5;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def download_nltk_resources():
    """Download required NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
        except:
            pass
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab', quiet=True)
        except:
            pass


def summarize_text(text, num_sentences=2):
    """
    Summarize text using extractive summarization.
    
    Args:
        text (str): The text to summarize
        num_sentences (int): Number of sentences in the summary
    
    Returns:
        str: The summarized text
    """
    if not text.strip():
        return None
    
    try:
        download_nltk_resources()
        
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text.lower())
        
        filtered_words = [
            word for word in word_tokens 
            if word.isalnum() and word not in stop_words
        ]
        
        word_freq = Counter(filtered_words)
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            for word in words:
                if word in word_freq:
                    sentence_scores[i] = sentence_scores.get(i, 0) + word_freq[word]
        
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        summary = ' '.join([sentences[i] for i, score in top_sentences])
        return summary
        
    except Exception as e:
        return None


# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 📝 AI Text Summarizer")
    st.markdown("**Instantly transform long texts into concise summaries powered by intelligent NLP**")

with col2:
    st.markdown("")
    st.markdown("")
    st.markdown('<span class="badge">✨ Powered by NLTK</span>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar Configuration
st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("Customize your summarization experience")

num_sentences = st.sidebar.slider(
    "📊 Summary Length",
    min_value=1,
    max_value=10,
    value=2,
    help="Choose how many sentences you want in the summary",
    key="sentences_slider"
)

st.sidebar.markdown("---")

# Example texts
st.sidebar.markdown("## 📚 Example Texts")
example_choice = st.sidebar.selectbox(
    "Choose an example to try:",
    [
        "Custom Text",
        "Technology",
        "Climate Change",
        "Space Exploration"
    ]
)

examples = {
    "Technology": "Artificial Intelligence is transforming the world by enabling machines to learn from data. AI systems can now recognize patterns, make predictions, and automate complex tasks. From healthcare to finance, AI is improving efficiency and creating new opportunities. Machine learning algorithms power recommendation systems, autonomous vehicles, and medical diagnostics. Natural language processing allows computers to understand and generate human language. Deep learning neural networks have achieved remarkable results in image recognition and language translation.",
    
    "Climate Change": "Climate change represents one of the most pressing challenges of our time. Rising global temperatures are causing unprecedented changes to our planet's ecosystems. Melting ice caps, rising sea levels, and extreme weather events are becoming increasingly common. Human activities, particularly the burning of fossil fuels, have significantly contributed to greenhouse gas emissions. Scientists worldwide agree that immediate action is necessary to reduce carbon emissions and transition to renewable energy sources. Governments and organizations are working together to develop sustainable solutions and protect our planet for future generations.",
    
    "Space Exploration": "Space exploration has always captivated human imagination. From the first satellite launches to manned moon missions, humanity has achieved remarkable milestones in space. Modern space agencies continue to push boundaries with advanced telescopes, rovers, and spacecraft. The search for life beyond Earth remains a key objective for space missions. International cooperation has become essential in conducting complex and expensive space research. Private companies are now playing a significant role in making space travel more accessible and affordable."
}

# Main Content Area
st.markdown("## 📥 Input")

# Initialize text_input
text_input = ""

# Input section with tabs
tab1, tab2 = st.tabs(["📝 Text Input", "📋 Examples"])

with tab1:
    text_input = st.text_area(
        "Paste your text here:",
        height=250,
        placeholder="Enter the text you want to summarize...",
        label_visibility="collapsed"
    )

with tab2:
    st.markdown("### Quick Examples")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔬 Technology Example", use_container_width=True):
            st.session_state.selected_example = "Technology"
            st.rerun()
    
    with col2:
        if st.button("🌍 Climate Example", use_container_width=True):
            st.session_state.selected_example = "Climate Change"
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🚀 Space Example", use_container_width=True):
            st.session_state.selected_example = "Space Exploration"
            st.rerun()
    
    with col4:
        if st.button("✏️ Use Custom", use_container_width=True):
            st.session_state.selected_example = "Custom Text"
            st.rerun()
    
    st.markdown("---")
    
    # Show selected example
    if "selected_example" in st.session_state:
        example_choice = st.session_state.selected_example
        if example_choice != "Custom Text" and example_choice in examples:
            st.markdown(f"### Selected: {example_choice}")
            st.info(examples[example_choice])
    else:
        st.info("👈 Click an example button to view it here")

st.markdown("---")

# Action buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("")

with col2:
    summarize_button = st.button("✨ Generate Summary", use_container_width=True, key="summarize_btn")

with col3:
    st.markdown("")

st.markdown("---")

# Output Section
if summarize_button:
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to summarize!")
    else:
        with st.spinner("🔄 Processing your text..."):
            summary = summarize_text(text_input, num_sentences)
            
            if summary:
                st.success("✅ Summarization Complete!")
                
                # Results section
                st.markdown("## 📊 Results")
                
                results_col1, results_col2 = st.columns(2)
                
                with results_col1:
                    st.markdown("### 📖 Original Text")
                    st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #6366f1; padding: 1.5rem; border-radius: 8px;">
                        {text_input}
                    </div>
                    """, unsafe_allow_html=True)
                
                with results_col2:
                    st.markdown("### 📄 Summary")
                    st.markdown(f"""
                    <div style="background: #ecfdf5; border-left: 4px solid #10b981; padding: 1.5rem; border-radius: 8px;">
                        <strong>{summary}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Statistics
                st.markdown("---")
                st.markdown("## 📈 Analysis")
                
                original_words = len(text_input.split())
                original_chars = len(text_input)
                original_sentences = len(sent_tokenize(text_input))
                
                summary_words = len(summary.split())
                summary_chars = len(summary)
                summary_sentences = len(sent_tokenize(summary))
                
                reduction = round((1 - summary_words/original_words) * 100, 1)
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Original Words</div>
                        <div class="metric-value">{original_words}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with stat_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Summary Words</div>
                        <div class="metric-value">{summary_words}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with stat_col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Reduction</div>
                        <div class="metric-value">{reduction}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with stat_col4:
                    ratio = round(original_words/summary_words, 1)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Compression Ratio</div>
                        <div class="metric-value">{ratio}:1</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Detailed metrics
                st.markdown("### 📋 Detailed Breakdown")
                
                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                
                with detail_col1:
                    st.metric("Sentences", f"{original_sentences} → {summary_sentences}")
                with detail_col2:
                    st.metric("Characters", f"{original_chars:,} → {summary_chars:,}")
                with detail_col3:
                    char_reduction = round((1 - summary_chars/original_chars) * 100, 1)
                    st.metric("Char Reduction", f"{char_reduction}%")
                with detail_col4:
                    st.metric("Avg Words/Sentence", f"{round(original_words/original_sentences)} → {round(summary_words/summary_sentences)}")
                
                st.markdown("---")
                
                # Download options
                st.markdown("## 💾 Export Options")
                
                download_col1, download_col2 = st.columns(2)
                
                with download_col1:
                    st.download_button(
                        label="📥 Download Summary (TXT)",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with download_col2:
                    combined_text = f"ORIGINAL TEXT:\n{text_input}\n\n{'='*50}\n\nSUMMARY:\n{summary}\n\n{'='*50}\n\nREDUCTION: {reduction}%"
                    st.download_button(
                        label="📥 Download Full Report",
                        data=combined_text,
                        file_name="summarization_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error("❌ Failed to generate summary. Please try again with different text.")

# Footer
st.markdown("""
    <div class="footer">
        <p>🚀 <strong>AI Text Summarizer</strong> | Powered by NLTK & Streamlit</p>
        <p>Transforming long-form content into actionable summaries | Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
