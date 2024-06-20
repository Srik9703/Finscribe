from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Make sure to install langchain
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
#from langchain_community.llms.HuggingFaceHub import HuggingFaceHub
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
import os
from pathlib import Path


if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
  token = "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"
  os.environ["HUGGINGFACEHUB_API_TOKEN"] = token

def text_loader(file_paths):
    documents = []
    for file_path in file_paths:
        if file_path.endswith('.txt'):
            loader = TextLoader(file_path)
            p = loader.load()
            documents+=p
        if file_path.endswith('.pdf'):
            loader=PyPDFLoader(file_path)
            p = loader.load_and_split()
            documents+=p
        
    return documents


def text_splitter(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs


def create_embeddings(docs):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    return db


def qa_chain(db,docs,query):
    llm=HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.1, max_length=512)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query)
    #chain.run(input_documents=docs, question=query)
    return (chain.run(input_documents=docs, question=query))


st.title("Document Query System")

# File uploader
uploaded_files = st.file_uploader("Upload Text or PDF Files", type=['txt', 'pdf'], accept_multiple_files=True)

if uploaded_files:
    # Create a directory to store the uploaded files
    upload_dir = "uploaded_files"
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    # Save uploaded files
    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb') as file:
            file.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
    #st.write(file_paths)
    # Load documents
    documents = text_loader(file_paths)
    st.write("Documents loaded successfully.")

    # Split documents into chunks
    docs = text_splitter(documents)
    #st.write("Documents split into chunks.")

    # Create embeddings
    db = create_embeddings(docs)
    #st.write("Embeddings created.")

    # User query input
    query = st.text_input("Enter query")

    if query:
        # Get the answer from the QA chain
        answer = qa_chain(db, docs, query)
        st.write("Answer:", answer)