import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

# packages from langchain
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks.manager import get_openai_callback


# load environment variables from .env file
load_dotenv()  

# Access the environment variable
key=os.getenv("OPENAI_API_KEY")


llm=ChatOpenAI(openai_api_key=key,tiktoken_model_name="gpt-3.5-turbo", temperature=0.5)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to conforming the text as well.
Make sure to format your responses like RESPONSE_JSON below and use is as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""


quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert english grammar and writer. Given a multiple Choise Quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analisis of the quiz.
Only use at max 50 words for complexity if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz wuestions wich needs to be changed and change the tone such that it perfectly fits the students.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# This is an overll chain where we call 2 chains in sequence
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], 
                        input_variables=["text","number", "subject", "tone", "response_json"], 
                        output_variables=["quiz", "review"], 
                        verbose=True)