import streamlit as st 

import os 
from dotenv import load_dotenv
load_dotenv()

from app.ui import pdf_uploader 
from app.pdf_utils import load_documents_from_pdfs,get_document_chunks
from app.chat_utils import get_chat_model,ask_chat_model
from app.vectorstore_utils import create_faiss_index, retrieve_relevant_docs
from tools_api import summarize_text, translate_text_auto, wiki_summary, web_search_langchain
EURI_API_KEY= st.secrets['EURI_API_KEY']

import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="BidEval Pro - RAG Powered Bid Evaluation",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet')

    html, body, [class*="st-"] {
        font-family: 'Roboto', sans-serif;
        font-size: 1.0rem;
    }

    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }

    /* Full dark sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
        color: #f1f1f1;
        border-right: 1px solid #333333;
        padding: 1rem;
    }

    /* Keep sidebar text and elements styled */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] .stButton {
        color: #f1f1f1;
    }

    /* Removed boxed sections */
    .sidebar-box {
        background: none !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        width: 100%;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(0, 123, 255, 0.3);
    }

    /* Chat input bar */
    [data-testid="stChatInput"] {
        background-color: #1E1E1E;
        border-top: 1px solid #333333;
    }

    /* Chat bubbles */
    .st-emotion-cache-janbn0 {
        border-radius: 8px;
        padding: 10px 14px;
        box-shadow: none;
        border: none;
    }

    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-user"]) {
        justify-content: end;
        display: flex;
    }

    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-user"]) .st-emotion-cache-janbn0 {
        background-color: #007BFF;
        color: white;
    }

    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-assistant"]) .st-emotion-cache-janbn0 {
        background-color: #2c2c2c;
        color: #F1F1F1;
    }
</style>
""", unsafe_allow_html=True)


# --- HEADER (DARK THEME) ---
st.markdown("""
<div style="text-align: center; padding: 0.5rem 0 1.5rem 0;">
    <h1 style="color: #00A6FB; font-size: 3.2rem; font-weight: 700;">Bid Evaluation </h1>
    <p style="font-size: 1.5rem; color: #A9A9A9;">Your Intelligent Bid Evaluation Assistant</p>
</div>
""", unsafe_allow_html=True)


## ---- UPLOAD PDFS ----

with st.sidebar:

    st.markdown(" ### 📂 Upload Bid Documents")
    st.caption("Upload one or more PDF files for evaluation")

    uploaded_files= pdf_uploader()

    if uploaded_files:
        st.success(f" {len(uploaded_files)} PDF files uploaded successfully.")
    
    st.divider()

    ## PROCESSING PDFS

    if uploaded_files:
        st.markdown("### ⚙️ Processing Documents")
        st.caption("Extract, chunk and index documents for efficient retrieval")

        if st.button("🚀 Start Processing", type="primary", use_container_width=True):
            with st.spinner("🔄 Analyzing and indexing bid documents..."):
                all_documents=load_documents_from_pdfs(uploaded_files)
                documents= get_document_chunks(all_documents)
                vectorstore=create_faiss_index(documents)
                st.session_state.vectorstore=vectorstore

                chat_model=get_chat_model(EURI_API_KEY)
                st.session_state.chat_model=chat_model

                st.success("✅ Documents processed and ready for Q&A")


st.markdown("----")

st.markdown("### Chat with your Bid Documents")

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore=None

if "chat_model" not in st.session_state:
    st.session_state.chat_model=None

if not st.session_state.messages:
    st.session_state.messages.append({
        "role":"assistant",
        "content":" Hello! How can I help you with your bid documents?"
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

## ------- AGENT ROUTING FUNCTION ------
def route_query(llm_model, query):
    routing_prompt= f"""
    You are an intelligent router for a multi-agent system. Based on the user's question, decide which tool to use:
    - RAG (default): for questions about uploaded bid documents
    - Summarizer: if the user wants a summary
    - Translator: if the user wants text translated
    - Wikipedia: if the user wants general knowledge
    - Web Search: if the user wants real-time web results

User query : "{query}"

Respond with ONLY the tool name: RAG, Summarizer, Translator, Wikipedia, or Web Search.
"""

    tool_choice= llm_model.invoke(routing_prompt).content
    return tool_choice.strip()

## ----- CHAT INPUT HANDLING ------- 

# As I want to use the user query to make LLM understand which tool to use, so I have to define the tools above that only.
if prompt:= st.chat_input ("Ask a question about your bid documents"):
    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("Searching for relevant documents..."):

                ## NOW IS THE TIME FOR AGENT ROUTING.... ONCE THE QUERY IS SENT TO THE LLM

                #------ Agent Routing -----
                selected_tool= route_query(st.session_state.chat_model, prompt)

                ## ---- Execute the selected tool ----
                response=""

                if selected_tool == "Summarizer":
                    response = summarize_text(st.session_state.chat_model, prompt)

                elif selected_tool == "Translator":
                    response = translate_text_auto(st.session_state.chat_model, prompt, prompt)

                elif selected_tool == "Wikipedia":
                    response = wiki_summary(prompt)

                elif selected_tool == "Web Search":
                    response = web_search_langchain(prompt)

                else: ## RAG by default 

                    context_docs=retrieve_relevant_docs(st.session_state.vectorstore, prompt)

                    if context_docs:
                        st.write("Found relevant documents:")
                        context_text="\n\n".join([doc.page_content for doc in context_docs])
                        full_prompt=f"""Based on this context:{context_text}\n\n Answer this question: {prompt}"""
                        response=ask_chat_model(st.session_state.chat_model, full_prompt)

                    else:
                        st.write("No relevant documents found. Please try another question.")

                st.markdown(response)

                st.session_state.messages.append({
                    "role":"assistant",
                    "content":response
                                        })
    else:
        st.session_state.messages.append({
            "role":"assistant",
            "content":"I'm sorry, but I can't process your request at the moment. Please try again later."
        })

        with st.chat_message("assistant"):
            st.error("Please upload bid documents in the sidebar first.")