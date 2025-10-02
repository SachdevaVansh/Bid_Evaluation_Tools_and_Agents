from euriai.langchain import create_chat_model

def get_chat_model(api_key:str):
    return create_chat_model(api_key=api_key,
                            model="gpt-5-mini-2025-08-07",
                            temperature=0.7)

def ask_chat_model(chat_model,prompt:str):
    response=chat_model.invoke(prompt)
    return response.content 