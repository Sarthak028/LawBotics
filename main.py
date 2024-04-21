
'''pip install openai
pip install unstructured
pip install langchain
pip install chromadb
pip install pypdf 
pip install tiktoken'''


import openai
import unstructured
import langchain
import chromadb
import pypdf
import nltk

import os
os.environ["OPENAI_API_KEY"]= "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"

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

loader = DirectoryLoader("data",glob="*.txt")
documents = loader.load()



from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever())

chat_history = []

def answer_question(question):
    global chat_history
    result = chain({"question": question, "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    return result['answer']

import gradio as gr

iface = gr.Interface(
    fn=answer_question,
    inputs="text",
    outputs="text",
    title="Barrister.ai",
    description="Ask any questions related to the legal procedures and judiciary of India"
)

iface.launch(share=True)