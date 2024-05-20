import os

import streamlit as st
from langchain.chains import RetrievalQA
from langchain.callbacks.base import BaseCallbackHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Neo4jVector
from neo4j import GraphDatabase
from streamlit.logger import get_logger
from commons import (
    load_embedding_model,
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

prompt = PromptTemplate(
    template="""\
You are an expert programmer and problem-solver, tasked with answering any question \
about Alfresco and Hyland products.

Generate a comprehensive and informative answer of 80 words or less for the \
given question based solely on the provided search results. You must \
only use information from the provided search results. Use an unbiased and \
journalistic tone. Combine search results together into a coherent answer. Do not \
repeat text. Only cite the most \
relevant results that answer the question accurately. Place these citations at the end \
of the sentence or paragraph that reference them - do not put them all at the end. If \
different results refer to different entities within the same name, write separate \
answers for each entity.

Never provide medical, legal, or financial advice. If the question asks for this \
information, say "I'm sorry, I'm unable to provide that information." If the question \
asks for personal opinions, say "I'm sorry, I'm unable to provide personal opinions."

Never try to embed links or images in your answer, unless they're from external websites.

If multiple versions of the software are mentioned in the search results, you should \
assume the most recent version is the one being referred to unless the question specifies \
a different version.

You should use bullet points in your answer for readability. Put citations where they apply \
rather than putting them all at the end.

If there is nothing in the context relevant to the question at hand, just say "I'm sorry, I'm \
unable to find that information." Don't try to make up an answer.

Anything between the following `context`  html blocks is retrieved from a knowledge \
bank, not part of the conversation with the user. 

<context>
    {context} 
<context/>

REMEMBER: if there is no relevant information within the context, just say "I'm sorry, I'm \
unable to find that information." Don't try to make up an answer. Anything between the preceding 'context' \
html blocks is retrieved from a knowledge bank, not part of the conversation with the \
user.\

Question: {question}
""", 
    input_variables=["question"]
)


embeddings, dimension = load_embedding_model(
    embedding_model_name, config={"ollama_base_url": ollama_base_url}, logger=logger
)


driver = GraphDatabase.driver(url, auth=(username, password))


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

def check_index_exists(session, index_name):
    result = session.run("SHOW INDEXES")
    for record in result:
        if record["name"] == index_name:
            return True
    return False

@st.cache_resource
def init_chains():
    llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})

    # For each markdown file under the initial-load folder,
    # split the text into chunks and store them in the db
    qa_chains = {}
    for file in os.listdir("initial-load"):
        with open(os.path.join("initial-load", file), "rb") as md:
            identifier = file[:-3] # remove the .md extension
            index_name = f"{identifier.replace('-', '')}"
            index_exists = False
            with driver.session() as session:
                index_exists = check_index_exists(session, index_name)

            if index_exists:
                print(f"Index {index_name} already exists, skipping initial load.")
                vectorstore = Neo4jVector.from_existing_index(
                    url=url,
                    username=username,
                    password=password,
                    embedding=embeddings,
                    index_name=index_name,
                    node_label=f"{identifier}_chunks",
                )
            else:
                print(f"Index {index_name} does not exist, starting initial load...")
                text = md.read().decode("utf-8")
                headers_to_split_on = [
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                    ("####", "Header 4"),
                    ("#####", "Header 5"),
                    ("######", "Header 6"),
                ]
                markdown_splitter = MarkdownHeaderTextSplitter(
                    headers_to_split_on=headers_to_split_on, strip_headers=False
                )
                md_header_splits = markdown_splitter.split_text(text)
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200, length_function=len
                )
                chunks = text_splitter.split_documents(md_header_splits)
                vectorstore = Neo4jVector.from_documents(
                    chunks,
                    url=url,
                    username=username,
                    password=password,
                    embedding=embeddings,
                    index_name=index_name,
                    node_label=f"{identifier}_chunks",
                    pre_delete_collection=True,
                )

            qa_chains[identifier] = RetrievalQA.from_chain_type(
                llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": prompt}
            )

    driver.close()
    return qa_chains

def main():
    qa_chains = init_chains()

    st.header("📚Chat with the Alfresco Docs!")
    st.header("👓Select the topic from the dropdown below:")
    topic = st.selectbox("Select a topic:", list(qa_chains.keys()), format_func=lambda x: x.replace("-", " ").title())

    # Accept user questions
    query = st.text_input("Ask a question about the selected topic:")

    if query and topic in qa_chains:
        stream_handler = StreamHandler(st.empty())
        qa_chains[topic].run({"query": query}, callbacks=[stream_handler])


if __name__ == "__main__":
    main()
