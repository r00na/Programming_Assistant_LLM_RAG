import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# Assuming 'vector' module and 'retriever' object are defined elsewhere
# from vector import retriever 
# Placeholder for retriever if 'vector.py' is not provided
class MockRetriever:
    def invoke(self, query):
        print(f"MockRetriever invoked with query: {query}")
        return ["Mock Q&A 1", "Mock Q&A 2"]
retriever = MockRetriever()

import time
# Removed base64 import as it's no longer needed for the image

# --- New Light Lavender/Lilac Color Scheme ---
background_color = "#F5F3F7"  # Very light lavender
primary_color = "#EAE4F0"     # Light lavender/gray (header/footer/question box)
accent_color = "#BCA8D1"      # Muted lavender/lilac (buttons/borders)
text_color = "#331C4B"        # Dark purple (main text)
input_bg_color = "#FFFFFF"    # White (input fields)
button_text_color = "#FFFFFF" # White (button text)
header_text_color = "#331C4B" # Dark purple (header text)
footer_text_color = "#5E4B70" # Medium purple (footer text)
input_border_color = accent_color # Use accent for input border

# --- Professional CSS with New Colors and Sticky Footer ---
st.markdown(f"""
<style>
    /* Main App Styling */
    .stApp {{
        background-color: {background_color};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
        /* Add padding to bottom to prevent content overlap with fixed footer */
        padding-bottom: 6rem; /* Adjust as needed based on footer height */
    }}

    /* Header Styling */
    header {{
        background-color: {primary_color};
        padding: 1.2rem;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: {header_text_color};
        border-bottom: 2px solid {accent_color};
        margin-bottom: 1.5rem; /* Add some space below header */
    }}

    /* Footer Styling - Sticky */
    footer {{
        background-color: {primary_color};
        padding: 1rem;
        text-align: center;
        color: {footer_text_color};
        font-size: 14px;
        border-top: 1px solid {accent_color};
        /* Sticky Footer Implementation */
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        z-index: 99;
    }}

    /* Text Input Styling */
    .stTextInput>div>div>input {{
        background-color: {input_bg_color};
        color: {text_color};
        border: 1px solid {input_border_color};
        border-radius: 6px;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: {accent_color};
        box-shadow: 0 0 0 1px {accent_color};
    }}

    /* Button Styling (Main Content & Sidebar) */
    .stButton>button {{
        background-color: {accent_color};
        color: {button_text_color};
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        border: none;
        transition: background-color 0.2s ease, color 0.2s ease; /* Add smooth transition */
    }}
    /* Remove Hover Effect Change for Buttons */
    .stButton>button:hover {{
        background-color: {accent_color} !important; /* Keep same background */
        color: {button_text_color} !important; /* Keep same text color */
        box-shadow: none !important; /* Remove default Streamlit hover shadow */
        transform: none !important; /* Prevent any slight movement */
    }}
    .stButton>button:active {{
        filter: brightness(0.95); /* Slight darkening on click */
    }}

    /* Question Answer Box Styling */
    .question-box {{
        background-color: {primary_color};
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        color: {text_color};
        border: 1px solid {accent_color};
        line-height: 1.6;
    }}

    /* Sidebar Styling */
    .stSidebar .stButton>button {{
        background-color: {accent_color};
        color: {button_text_color};
    }}
    .stSidebar .stButton>button:hover {{
        background-color: {accent_color} !important;
        color: {button_text_color} !important;
        box-shadow: none !important;
        transform: none !important;
    }}
    
    .stSidebar .stHeader {{
        color: {header_text_color};
    }}
    .stSidebar .stSubheader {{
        color: {header_text_color}; /* Style subheaders in sidebar */
    }}

    /* Expander Styling */
    .stExpander {{
        border: 1px solid {accent_color};
        border-radius: 8px;
        background-color: {background_color};
    }}
    .stExpander header {{
        background-color: transparent; /* Remove header background */
        border-bottom: none; /* Remove header border */
        padding: 0.5rem 1rem;
        font-size: 16px;
        color: {text_color};
    }}
   
    /* About Section Styling in Sidebar */
    .stSidebar .about-section {{
        background-color: {primary_color};
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid {accent_color};
        color: {text_color};
        line-height: 1.6;
        margin-bottom: 1rem; /* Add some space below */
    }}

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f'<header>Programming Assistant</header>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    # --- About Section (Moved to top of sidebar) ---
    st.subheader("About")
    # Use a CSS class for styling the about section
    st.markdown(f"""
    <div class='about-section'>
        <strong>Programming Assistant</strong> is an AI-powered application designed to help you with coding questions using examples from real Q&A.<br><br>
    </div>
    """, unsafe_allow_html=True)

    # --- Suggested Questions ---
    st.header(" Suggested Questions")
    questions_list = [
        "What is the difference between list and tuple?",
        "Explain Python decorators with example.",
        "How to handle missing values in pandas?",
        "What is a RESTful API?",
        "Difference between SQL and NoSQL databases?",
        "Explain OOP principles in Python.",
        "How to use FastAPI with SQLite?",
        "What is time complexity of bubble sort?",
        "What is the role of '__init__' in Python?",
        "Explain the difference between PUT and POST.",
        "What is multithreading in Python?",
    ]
    # Apply button styling implicitly via CSS
    for question in questions_list:
        if st.button(question, key=question): # Added unique keys for buttons
            st.session_state["question"] = question
            # Rerun to update the text input value immediately
            st.rerun()

# --- Model Setup ---
try:
    model = OllamaLLM(model="llama3:instruct")
except Exception as e:
    st.error(f"Failed to load Ollama model: {e}")
    model = None # Set model to None if loading fails

template = """
You are a senior programming assistant helping users understand StackOverflow questions and answers.

Here are some related programming Q&A examples:\n{reviews}

User's question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

if model:
    chain = prompt | model
else:
    chain = None # No chain if model failed

# --- Main Page Content ---
st.markdown("## Ask Your Programming Question Below")

# Initialize session state for question if it doesn't exist
if "question" not in st.session_state:
    st.session_state["question"] = ""

# Use session state value for text input
question = st.text_input("Type your question:", value=st.session_state.question, label_visibility="collapsed", key="main_question_input")

# Update session state if text input changes
if question != st.session_state.question:
    st.session_state.question = question

if st.button("Submit Question", key="submit_button"):
    if not chain:
        st.error("Model is not available. Cannot process question.")
    elif question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner(" Processing your question..."):
            try:
                start_retrieval = time.time()
                reviews = retriever.invoke(question)
                end_retrieval = time.time()

                start_model = time.time()
                result = chain.invoke({"reviews": reviews, "question": question})
                end_model = time.time()

                st.markdown("###  Answer")
                st.markdown(f"<div class='question-box'>{result}</div>", unsafe_allow_html=True)

                with st.expander(" Debug Info"):
                    st.write(f"Retrieval time: {end_retrieval - start_retrieval:.2f} seconds")
                    st.write(f"Model response time: {end_model - start_model:.2f} seconds")
            except Exception as e:
                st.error(f"An error occurred while processing your question: {e}")

# --- Footer ---
st.markdown(f'<footer>© 2025 Rana Haitham Al-Raqad - All rights reserved.</footer>', unsafe_allow_html=True)

