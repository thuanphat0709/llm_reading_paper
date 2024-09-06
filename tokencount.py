import tiktoken
import constants
from constants import exam_tem, instruct_tem, input_tem
import os

DOCUMENT_MAP = constants.DOCUMENT_MAP
file_path = "robert2018.pdf"

def combine_documents(docs, separator: str = '\n\n') -> str:
    serialized_docs = [doc.page_content for doc in docs]
    return separator.join(serialized_docs)

# Loads a single document from a file path
file_path = f"docs/{file_path}"

file_name_split =  os.path.splitext(file_path)
file_extension = file_name_split[1]
filename = file_name_split[0][5:]
loader_class = DOCUMENT_MAP.get(file_extension)
if loader_class:
    docs = loader_class(file_path).load()
    # document = [doc.page_content for doc in docs]
    full_doc = combine_documents(docs)
    print(full_doc)
else:
    raise ValueError("Document type is undefined")


# Initialize the tokenizer for GPT-4 (or any other model)
tokenizer = tiktoken.encoding_for_model("gpt-4")

# Example text
text = exam_tem+ instruct_tem + input_tem + exam_tem + full_doc

# Count tokens
tokens = tokenizer.encode(full_doc)
print(f"Number of tokens: {len(tokens)}")