import logging
import os

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from constants import (
    DOCUMENT_MAP,
    PERSIST_DIRECTORY
)


def combine_documents(docs, separator: str = '\n\n') -> str:
    serialized_docs = [doc.page_content for doc in docs]
    return separator.join(serialized_docs)

def load_document(file_path: str) -> Document:
    # Loads a single document from a file path
    file_path = f"docs/{file_path}"
    try:
       file_name_split =  os.path.splitext(file_path)
       file_extension = file_name_split[1]
       loader_class = DOCUMENT_MAP.get(file_extension)
       if loader_class:
           logging.info(f"{file_path} loaded")
           docs = loader_class(file_path).load()
       else:
           logging.info(f"{file_path} document type is undefined")
           raise ValueError("Document type is undefined")
       return docs
    except Exception as ex:
       print(f"loading error: \n ({file_path}, {ex})")
       return None , None

def ingest_run(filepath):
    doc_list = load_document(filepath)
    full_doc = combine_documents(doc_list)
    return full_doc

# if __name__ == "__main__":
#     logging.basicConfig(
#         format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
#     )
#     a =  ingest_run(file_path)
#     print(a)
