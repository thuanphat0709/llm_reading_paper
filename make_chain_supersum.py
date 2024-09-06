from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
import json
import constants
from constants import input_tem_super, exam_tem_super, instruct_tem_super

EXAMPLE = exam_tem_super
INSTRUCTION = instruct_tem_super
QA_TEMPLATE = input_tem_super

def make_chain(context):    

    model = ChatOpenAI(
        temperature=0.2,  # increase temperature to get more creative answers
        model_name='gpt-4o-mini'  # change this to 'gpt-4' if you have access
    )

    # Create a PromptTemplate
    answer_prompt = PromptTemplate(
        input_variables=["document","instruct","example"],
        template=QA_TEMPLATE
    )
    # Create the LLMChain with the model and prompt
    llm_chain = answer_prompt | model

    # Define the input values
    input_values = {
        "document": context,
        "instruct": INSTRUCTION,
        "example": EXAMPLE
    }

    # Run the LLMChain with the inputs
    response = llm_chain.invoke(input_values).content

    return response