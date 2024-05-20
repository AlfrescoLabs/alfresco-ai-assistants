import os
import requests

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import tool
from langchain.tools.render import render_text_description
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from streamlit.logger import get_logger
from langchain.globals import set_debug
from operator import itemgetter
from commons import (
    load_llm,
)

# load api key lib
from dotenv import load_dotenv

load_dotenv(".env")


url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
llm_name = os.getenv("LLM")
alfresco_url = os.getenv("ALFRESCO_URL")
alfresco_username = os.getenv("ALFRESCO_USERNAME")
alfresco_password = os.getenv("ALFRESCO_PASSWORD")
# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url

logger = get_logger(__name__)
set_debug(True)

json_response_prompt = PromptTemplate(
    template="""You are an assistant that extracts relevant data from JSON, and translates that relevant data into natural language.
Anything between the following `json_response` html blocks is retrieved from a knowledge \
bank, not part of the conversation with the user.

<json_response>
    {json_response}
</json_response>

Your responses must include only the data that is relevant. Your responses must contain no JSON snippets nor syntax.
Don't include anything in the response other than the requested data, in natural language.

Generate a comprehensive and informative answer of 80 words or less for the \
given question based solely on the provided JSON response. Do not mention the JSON response in your answer.
Use formatting to make your answer more readable.

Question: {question}""",
 input_variables=["json_response", "question"])

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def discovery() -> dict:
    """Discover the current Alfresco Content Services version, installed modules, and license status."""
    url = f"{alfresco_url}/alfresco/api/discovery"
    return requests.get(url, auth=(alfresco_username, alfresco_password)).json()

tools = [multiply, discovery]
rendered_tools = render_text_description(tools)

system_prompt = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys.
The 'name' key should be the name of the tool to use, and the 'arguments' key should be a dictionary of the arguments to pass to the tool.
The 'arguments' key should be a dictionary with the argument names as keys and the argument values as values."""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool

def main():
    llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})
    chain = prompt | llm | JsonOutputParser() | tool_chain

    st.header("👨‍🔬I'm your Alfresco SDK AI Assistant!")

    # Accept user questions
    input = st.text_input("What do you want to do today? Ask me anything:")

    if input:
        response = chain.invoke({"input": input})
        if isinstance(response, dict):
            json_chain = json_response_prompt | llm | StrOutputParser()
            response = json_chain.stream({"json_response": response, "question": input})
            st.write_stream(response)
        else:
            st.write(response)


if __name__ == "__main__":
    main()
