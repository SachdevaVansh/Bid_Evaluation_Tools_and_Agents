# 📑 BidEval Pro – Advanced RAG-Powered Bid Evaluation with Agent Tools

BidEval Pro is an advanced AI-powered assistant for intelligent bid document evaluation.
It combines RAG (Retrieval-Augmented Generation) with multi-agent tool integration to enable smarter, context-aware interactions with bid PDFs and external sources.

Users can upload multiple bid documents, process them into searchable embeddings, and interact with them through a conversational interface. With the new Agent Routing system, the assistant automatically selects the right tool for each query — whether it’s retrieving from bid docs, summarizing, translating, fetching from Wikipedia, or performing a web search.

🚀 Features

📂 Upload Bid PDFs: Upload multiple bid documents for evaluation.

⚡ Automatic Preprocessing: Extracts, chunks, and indexes PDFs into a FAISS vector store.

🤖 Chat Assistant with RAG: Ask natural language questions and get context-driven answers from your documents.

🧠 Agent Routing: Dynamically routes queries to the best tool:

RAG → Default, for bid document Q&A

Summarizer → Generates summaries of text/documents

Translator → Automatically translates text into target language

Wikipedia → Retrieves knowledge from Wikipedia

Web Search → Fetches real-time web results

🎨 Modern Dark-Theme UI: Custom-styled Streamlit interface with chat bubbles, styled sidebar, and interactive elements.

🔍 Context Transparency: Displays which documents were used for generating answers.

🛠️ Tech Stack

Streamlit
 – Interactive web UI

LangChain
 – Document loading, chunking, retrieval, and routing

FAISS
 – Vector database for semantic search

dotenv
 – Environment variable management

### Custom Tool Integrations

#### summarize_text – Summarization utility

#### translate_text_auto – Language translation utility

#### wiki_summary – Wikipedia lookup

#### web_search_langchain – Real-time web search

📂 Project Structure
.
├── app/
│   ├── ui.py                  # PDF uploader
│   ├── pdf_utils.py           # PDF extraction & chunking
│   ├── chat_utils.py          # Chat model integration
│   ├── vectorstore_utils.py   # FAISS vector store utilities
├── tools_api.py               # External tools: Summarizer, Translator, Wiki, Web Search
├── app.py                     # Main Streamlit application
├── .env                       # Environment variables (not tracked)
├── requirements.txt           # Dependencies
└── README.md                  # Documentation

⚙️ Setup & Installation
1. Clone the repository
```bash
git clone https://github.com/SachdevaVansh/Bid_Evaluation_Tools_and_Agents.git
cd Bid_Evaluation_Tools_and_Agents
```
2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure API keys

Create a .env file in the root folder:
```bash
EURI_API_KEY=your_euri_api_key
```

Or configure via Streamlit secrets in .streamlit/secrets.toml:
```bash
EURI_API_KEY="your_euri_api_key"
```
5. Run the app
```bash
streamlit run app.py
```
📌 Usage Workflow

Upload PDFs in the sidebar.

Click 🚀 Start Processing to analyze and index documents.

Ask natural language queries in the chat box.

The assistant automatically decides the best tool to handle the query:

Example 1: “Summarize the uploaded bids.” → Uses Summarizer

Example 2: “Translate the contract terms to French.” → Uses Translator

Example 3: “What is renewable energy policy in India?” → Uses Wikipedia

Example 4: “Latest steel price trends 2025.” → Uses Web Search

Example 5: “What are the payment terms in this bid?” → Uses RAG on uploaded PDFs

✅ Requirements

Python 3.9+

Streamlit

LangChain

FAISS

python-dotenv

(Include all in requirements.txt)

🎨 UI Highlights

Sidebar for file uploads & processing

Modern dark theme

Chat with styled user (blue) and assistant (gray) bubbles

Transparent feedback on document retrieval & tool selection

📜 License

This project is licensed under the MIT License.
Feel free to use, extend, and modify it for your own projects.
