
# Load docs
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.vectorstores import Chroma
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
os.environ['USER_AGENT'] = 'myagent'
import json

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Loads the latest version
# prompt = hub.pull("rlm/rag-prompt", api_url="https://api.hub.langchain.com")


prompt = ChatPromptTemplate.from_messages([
    ("system", 
        """
            You are an expert for question answering tasks. Use the retrieved context {context} if available to answer the question. 
            If not available, answer to the best of your knowledge. Provide the answer concisely in a maximum of 3 sentences. Use bullet points if required
        """
    ),
    ("user", "{question}")
])
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", """
     You are a networking expert who answers networking or telecom domain related questions. If retrieved context {context} is not empty, use it to answer the question. 
     Provide the answer concisely in a maximum of 5 sentences. Use bullet points if required. Politely refuse to answer questions that are off topic.  
     """),
    ("user", "{input}")
])

# LLM
llm = OllamaLLM(model="llama3", temperature=0)

config = RailsConfig.from_path("./config")
guardrails = RunnableRails(config)

output_parser = StrOutputParser()

# simple_chain = simple_prompt | llm | output_parser

# updated_simple_chain = guardrails | simple_chain

# question = "What are the approaches to Task Decomposition?"
# # question = "Describe Indian flag"

# result = updated_simple_chain.invoke({"input":  question, "context": ""})
# print(question + " : " + result)


# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
loader = WebBaseLoader("https://www.geeksforgeeks.org/basics-computer-networking/")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Store splits

oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="all-minilm")

vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

# RetrievalQA
from langchain.chains import RetrievalQA

question = "What is a computer network?"
# question = "Describe Indian flag"

# qa_chain = RetrievalQA.from_chain_type(
#     llm, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": simple_prompt}
# )
qa_chain = (
{"context": vectorstore.as_retriever(), "input": RunnablePassthrough()}
| simple_prompt
| llm
| output_parser
)

# rails = LLMRails(config)
# response = rails.generate(messages=[{
#         "role": "user",
#         "content": question}])
# print(response)
# info = rails.explain()
# info.print_llm_calls_summary()
# print(info.colang_history)


updated_qa_chain =  guardrails | qa_chain 

query_list = [
              "Hello!",
              "How big is a football pitch?",
              "I know you are stupid.",
              "What is the difference between a switch and a router?",
              "sdaswerfdsfdsf",
              "How to make a cake?",
              "What is the maximum bandwidth offered in 5G network?",
              "Describe Indian flag?",
              "Briefly tell me about computer network architecture",
              "Which city has the best metro rail network?",
              "How does a DNS server work?",
              "Tell me about satellites launched by ISRO?",
              "How is the weather in Goa today?",
              "When was computer network first developed and for what purposes?"
              
]

for query in query_list:
    result = updated_qa_chain.invoke({"input": query})
    print(query + " :: " + json.dumps(result))
