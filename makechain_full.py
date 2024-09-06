from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
import json
import ingest_full
import constants
from constants import exam_tem, instruct_tem, input_tem, query
import json

QUERY = query

EXAMPLE = exam_tem
INSTRUCTION = instruct_tem
QA_TEMPLATE = input_tem

source_dir = "docs"

def make_chain(document):    

    model = ChatOpenAI(
        temperature=0.2,  # increase temperature to get more creative answers
        model_name='gpt-4o-mini'  # change this to 'gpt-4' if you have access
    )
    
    docs_to_read = document

    # Create a PromptTemplate
    answer_prompt = PromptTemplate(
        input_variables=["document","instruct","example"],
        template=QA_TEMPLATE
    )
    # Create the LLMChain with the model and prompt
    llm_chain = answer_prompt | model

    # Define the input values
    input_values = {
        "document": docs_to_read,
        "instruct": INSTRUCTION,
        "example": EXAMPLE
    }

    # Run the LLMChain with the inputs
    response = llm_chain.invoke(input_values).content

    return response

# if __name__ == "__main__":
#     response = make_chain(document)
#     result = json.loads(response)
#     print(result["Trading strategy"])