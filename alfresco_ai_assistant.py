import os
import uuid

from alfresco_api import *
from report_writer import ReportWriter
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
report_writer = ReportWriter()

DOCUMENT_NOT_FOUND = "Document not found. Please try again."
FOLDER_NOT_FOUND = "Folder not found. Please try again."

logger = get_logger(__name__)
set_debug(True)
llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})

redact_prompt = PromptTemplate(
    template="""Redact all references to {request} from the following document.
Replace the redacted information with the "[REDACTED]" placeholder.

Document: {to_redact}""",
 input_variables=["to_redact", "request"])

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
def redact_content(document_title: str, user_request: str) -> str:
    """Find and redact / censor the content of a document within Alfresco Content Services (ACS). The user can request specific information to be redacted."""
    document = get_document_content(document_title)
    if document == DOCUMENT_NOT_FOUND:
        return DOCUMENT_NOT_FOUND

    redact_chain = redact_prompt | llm | StrOutputParser()
    response = redact_chain.stream({"to_redact": document["content"], "request": user_request})
    st.write_stream(response)
    return None

@tool
def copy_file(filename: str, folder_name: str) -> dict:
    """Copy file within Alfresco Content Services (ACS) to the specified folder."""
    folders = search_api.search_folders_by_name(folder_name)
    try:
        folder_id = folders["list"]["entries"][0]["entry"]["id"]
        folder_name = folders["list"]["entries"][0]["entry"]["name"]
    except IndexError:
        return FOLDER_NOT_FOUND

    documents = search_api.search_by_name(filename)
    try:
        node_id = documents["list"]["entries"][0]["entry"]["id"]
    except IndexError:
        return DOCUMENT_NOT_FOUND

    response = node_api.copy_to_folder(node_id, folder_id)
    try:
        filename = response["entry"]["name"]
        return {"successfully_copied_file": filename, "destination_folder": folder_name}
    except KeyError:
        error = response["error"]
        return {"error": error}

@tool
def list_recent_content_snippets(search_term: str) -> dict:
    """Find and show the snippets of recent documents within Alfresco Content Services (ACS) that contain a certain search term."""
    response = search_api.search_recent_docs_snippets(search_term)
    entries = response["list"]["entries"]
    if not entries:
        return f"No recent documents found containing the search term '{search_term}'."

    # simplify the JSON response preserving only the relevant information
    results = {}
    for entry in entries:
        entry = {
            "file_name": entry["entry"]["name"],
            "created_date": entry["entry"]["createdAt"],
            "edited_date": entry["entry"]["modifiedAt"],
            "highlight_snippets": entry["entry"]["search"]["highlight"][0]["snippets"]
        }
        results[f"{entry['file_name']}_{uuid.uuid4()}"] = entry

    return results

@tool
def create_pdf_report(document_title: str, document_text: str) -> str:
    """Create a PDF report containing the given text content."""
    report_writer.write_report(document_title, document_text)
    node_api.upload_file(f"{document_title}.pdf", "8bb36efb-c26d-4d2b-9199-ab6922f53c28")
    return f'{document_title}.pdf created!'

tools = [discovery, transform_content, translate_content, redact_content, list_recent_content_snippets, copy_file, create_pdf_report]
rendered_tools = render_text_description(tools)

system_prompt = f"""You are a robot that only outputs JSON, and has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys.
The 'name' key should be the name of the tool to use, and the 'arguments' key should be a dictionary of the arguments to pass to the tool.
The 'arguments' key should be a dictionary with the argument names as keys and the argument values as values.
Only reply with the name and arguments of the tool to use. Do not include any other information in your response.
Do not include anything before or after the JSON blob. Do not mention that you are providing a JSON response, only provide the JSON blob and nothing else."""

prompt_messages = [("system", system_prompt)]
example_messages = [
    ("user", "Is the Alfresco Content Services license up to date?"), ("assistant", '{{"name": "discovery", "arguments": {{}}}}'),
    ("user", "Summarise the content of the document titled 'minutes.docx'"), ("assistant", '{{"name": "transform_content", "arguments": {{"document_title": "minutes.docx"}}}}'),
    ("user", "Translate the content of the document titled 'minutes.docx' to French"), ("assistant", '{{"name": "translate_content", "arguments": {{"document_title": "minutes.docx", "language": "French"}}}}'),
    ("user", "Redact all mentions of colors and names in 'snowwhite.docx'"), ("assistant", '{{"name": "redact_content", "arguments": {{"document_title": "snowwhite.docx", "user_request": "colors, names"}}}}'),
    ("user", "Show snippets of recent documents that contain the term 'contract'"), ("assistant", '{{"name": "list_recent_content_snippets", "arguments": {{"search_term": "contract"}}}}'),
    ("user", "Copy 'minutes.docx' to the 'Board Meetings' folder"), ("assistant", '{{"name": "copy_file", "arguments": {{"filename": "minutes.docx", "folder_name": "Board Meetings"}}}}'),
]
prompt_messages += example_messages
prompt_messages.append(("user", "{input}"))

prompt = ChatPromptTemplate.from_messages(prompt_messages)

def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool

def main():
    chain = prompt | llm | JsonOutputParser() | tool_chain

    st.header("🤹‍♂️I'm Alfredo, your Alfresco AI Assistant!")

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
