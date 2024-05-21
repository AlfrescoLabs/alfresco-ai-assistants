import os

from alfresco_api import *
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

# API clients
search_api = AlfrescoSearchAPI(alfresco_url, alfresco_username, alfresco_password)
node_api = AlfrescoNodeAPI(alfresco_url, alfresco_username, alfresco_password)
discovery_api = AlfrescoDiscoveryAPI(alfresco_url, alfresco_username, alfresco_password)

DOCUMENT_NOT_FOUND = "Document not found. Please try again."
FOLDER_NOT_FOUND = "Folder not found. Please try again."

logger = get_logger(__name__)
set_debug(True)
llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})

translate_prompt = PromptTemplate(
    template="""Original: {to_translate}. {language}:""",
 input_variables=["to_translate", "language"])

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
The response must use the language required by the question and it must never mix different languages.

Question: {question}""",
 input_variables=["json_response", "question"])

def get_document_content(document_title: str) -> dict:
    search_response = search_api.search_by_name(document_title)
    try:
        node_id = search_response["list"]["entries"][0]["entry"]["id"]
    except IndexError:
        return DOCUMENT_NOT_FOUND

    response = node_api.get_node_content(node_id)
    return {"document_title": document_title, "content": response}

def copy_files_with_extension_to_folder(extension: str, folder_name: str) -> dict:
    search_response = search_api.get_folder_ids(folder_name)
    try:
        folder_id = search_response["list"]["entries"][0]["entry"]["id"]
    except IndexError:
        return FOLDER_NOT_FOUND

    search_response = search_api.get_nodes_ids_by_extension(extension)
    try:
        node_ids = [entry["entry"]["id"] for entry in (search_response)["list"]["entries"]]
    except KeyError:
        return DOCUMENT_NOT_FOUND

    copied_files = []
    errors = []
    for node_id in node_ids:
        response = node_api.copy_to_folder(node_id, folder_id)
        try:
            filename = response["entry"]["name"]
            copied_files.append({"copied_filename": filename})
        except KeyError:
            error = response["error"]
            errors.append({"error": error})

    return {"copied_files_successfully": copied_files, "errors": errors}

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def discovery() -> dict:
    """Discover the current Alfresco Content Services (ACS) version, installed modules, and license status."""
    return discovery_api.get_repository_info()

@tool
def transform_content(document_title: str) -> dict:
    """Find and transform (e.g.: summarise, classify) the content of a document within Alfresco Content Services (ACS)."""
    return get_document_content(document_title)

@tool
def translate_content(document_title: str, language: str) -> str:
    """Find and translate the content of a document within Alfresco Content Services (ACS)."""
    document = get_document_content(document_title)
    if document == DOCUMENT_NOT_FOUND:
        return DOCUMENT_NOT_FOUND
    
    translate_chain = translate_prompt | llm | StrOutputParser()
    response = translate_chain.stream({"to_translate": document["content"], "language": language})
    st.write_stream(response)
    return None

@tool
def copy_files_to_folder(extension: str, folder_name: str) -> dict:
    """Copy files with the given extension to given folder and return the names of files that were successfully copied and describe all errors."""
    return copy_files_with_extension_to_folder(extension, folder_name)


tools = [multiply, discovery, transform_content, translate_content, copy_files_to_folder]
rendered_tools = render_text_description(tools)

system_prompt = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys.
The 'name' key should be the name of the tool to use, and the 'arguments' key should be a dictionary of the arguments to pass to the tool.
The 'arguments' key should be a dictionary with the argument names as keys and the argument values as values.
Only reply with the name and arguments of the tool to use. Do not include any other information in your response.
Do not include anything before or after the JSON blob."""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool

def main():
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
        elif response:
            st.write(response)


if __name__ == "__main__":
    main()
