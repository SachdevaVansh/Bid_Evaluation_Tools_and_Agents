from transformers import pipeline 
import wikipedia
#from googlesearch import search 

from langchain.tools import DuckDuckGoSearchRun

## Summarizer
summarizer= pipeline("summarization")

def summarize_text(text, max_length=300):
    return summarizer(text,max_length=max_length, min_length=50, do_sample=False)[0]['summary_text']

## Translator

## Mapping ISO codes to Hugging Face models
LANG_MODEL_MAP={
    "ta": "ai4bharat/opus-mt-en-tam",  # Tamil
    "te": "ai4bharat/opus-mt-en-tel",  # Telugu
    "hi": "Helsinki-NLP/opus-mt-en-hi", # Hindi
    "bn": "Helsinki-NLP/opus-mt-en-bn", # Bengali
    "mr": "Helsinki-NLP/opus-mt-en-mr", # Marathi
    "fr": "Helsinki-NLP/opus-mt-en-fr", # French
    "es": "Helsinki-NLP/opus-mt-en-es", # Spanish
}

## To prevent the model from not returining ISO codes, we use a regex to match the 2-letter ISO code.
import re 

def extract_target_language(llm_model, user_query):
    """ 
    Detect the target language from the user's query using LLM.
    Return 2 letter ISO code. Defaults to 'en" if not found."""

    prompt=f""" 
    Detect the target language from this user request and return only the 2-letter ISO language code.
    If no specific language is mentioned, return 'en'. 

    User query: "{user_query}"
    """
    try:
        lang_code=llm_model(prompt).strip().lower()
        # Ensure only 2 letters
        lang_code = re.findall(r"[a-z]{2}", lang_code)
        lang_code= lang_code[0] if lang_code else "en"
        if lang_code not in LANG_MODEL_MAP:
            return "en"
        return lang_code
    except:
        return "en"

#Currently, each translation call initializes a new Hugging Face pipeline. This can be slow.

#Suggestion: Initialize a translator pipeline per language once and cache it.

#Preload the translators
TRANSLATOR_CACHE={}

def translate_text_auto(llm_model,text, user_query):
    """
    Translate 'text' to the language specified in 'user_query'.
    Uses LLM to detect target language and selects the correct translation model.
    """
    target_lang= extract_target_language(llm_model,user_query)

    if target_lang =="en":
        return text

    model_name= LANG_MODEL_MAP.get(target_lang)
    if not model_name:
        return f"Sorry , translation to '{target_lang}' is not supported."

    ## Use the cached pipeline if it exists 
    if target_lang not in TRANSLATOR_CACHE:
        try:
            TRANSLATOR_CACHE[target_lang]=pipeline("translation", model=model_name)
        except Exception as e:
            return f"Translation pipeline failed to load: {e}"

    try:
        translator=TRANSLATOR_CACHE[target_lang]
        translated_text=translator(text)[0]['translation_text']
        return translated_text

    except Exception as e:
        return f"Translation failed due to error: {str(e)}"

## Wikipedia 
def wiki_summary(query,sentences=3):
    try:
        return wikipedia.summary(query, sentences=sentences)
    except:
        return "No wikipedia information found"

## Web search using Duckduckgo
duck_tool= DuckDuckGoSearchRun()

def web_search_langchain(query, max_results=3):
    """
    Perform a web search using LangChain's DuckDuckGoSearch tool.
    Returns aggregated snippets from top results.
    """
    search_results=duck_tool.run(query)

    # Optional: truncate long results
    if isinstance(search_results, str):
        # Split by newlines or sentences to pick top few
        lines = search_results.split("\n")
        return "\n".join(lines[:max_results])

    return search_results