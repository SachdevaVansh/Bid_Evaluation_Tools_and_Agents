import os 
import tempfile 
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter 

def load_documents_from_pdfs(pdf_files):
    all_documents=[]

    for pdf_file in pdf_files:
        temp_file_path=""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_file.getvalue())
                temp_file_path=temp_file.name
            
            loader=PyPDFLoader(temp_file_path)
            documents=loader.load()
            all_documents.extend(documents)

        except Exception as e:
            print(f"Error processing file {pdf_file.name} : {e}")

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    return all_documents

def get_document_chunks(documents):
    if not documents:
        return []

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30,length_function=len)

    chunks=text_splitter.split_documents(documents)
    return chunks 
    
