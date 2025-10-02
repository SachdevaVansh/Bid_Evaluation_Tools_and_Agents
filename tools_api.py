import wikipedia
from langchain.tools import DuckDuckGoSearchRun

# --- Summarizer using LLM (via EURI API) ---
def summarize_text(llm_model, text, max_length=300):
    """
    Summarize text using the LLM API (Euri).
    """
    prompt = f"""
    Summarize the following text in less than {max_length} words:
    
    {text}
    """
    try:
        summary = llm_model.invoke(prompt).content.strip()
        return summary
    except Exception as e:
        return f"Summarization failed: {str(e)}"


# --- Translator using LLM (via EURI API) ---
import re

# ISO language support map (for validation only, not needed for API call itself)
LANG_CODES = ["ta", "te", "hi", "bn", "mr", "fr", "es", "en"]

def extract_target_language(llm_model, user_query):
    """
    Detect the target language from the user's query using LLM.
    Return 2-letter ISO code. Defaults to 'en'.
    """
    prompt = f"""
    Detect the target language from this user request and return only the 2-letter ISO language code.
    If no specific language is mentioned, return 'en'.

    User query: "{user_query}"
    """
    try:
        lang_code = llm_model.invoke(prompt).content.strip().lower()
        # Ensure only 2 letters
        lang_code = re.findall(r"[a-z]{2}", lang_code)
        lang_code = lang_code[0] if lang_code else "en"
        if lang_code not in LANG_CODES:
            return "en"
        return lang_code
    except:
        return "en"

def translate_text_auto(llm_model, text, user_query):
    """
    Translate 'text' to the language specified in 'user_query'.
    Uses LLM (Euri API) for translation.
    """
    target_lang = extract_target_language(llm_model, user_query)

    if target_lang == "en":
        return text

    prompt = f"""
    Translate the following text into {target_lang}:

    {text}
    """
    try:
        translated = llm_model.invoke(prompt).content.strip()
        return translated
    except Exception as e:
        return f"Translation failed: {str(e)}"


# --- Wikipedia ---
def wiki_summary(query, sentences=3):
    try:
        return wikipedia.summary(query, sentences=sentences)
    except:
        return "No wikipedia information found"


# --- Web search using DuckDuckGo ---
duck_tool = DuckDuckGoSearchRun()

def web_search_langchain(query, max_results=3):
    """
    Perform a web search using LangChain's DuckDuckGoSearch tool.
    Returns aggregated snippets from top results.
    """
    search_results = duck_tool.run(query)

    # Optional: truncate long results
    if isinstance(search_results, str):
        lines = search_results.split("\n")
        return "\n".join(lines[:max_results])

    return search_results
