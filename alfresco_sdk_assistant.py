import os

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.tools.render import render_text_description
from langchain_core.output_parsers import JsonOutputParser
from streamlit.logger import get_logger
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
# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url

logger = get_logger(__name__)

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

tools = [multiply]
rendered_tools = render_text_description(tools)

system_prompt = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys."""

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
        st.write(response)


if __name__ == "__main__":
    main()
