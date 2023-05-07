import os
import openai
from llama_index import OpenAIEmbedding, ServiceContext, SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from llama_index.node_parser import SimpleNodeParser
from langchain.text_splitter import TokenTextSplitter
import tiktoken
from config import Config

openai.api_key = Config.OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = Config.OPENAI_API_KEY
UPLOAD_FOLDER = 'uploads'

enc = tiktoken.get_encoding("cl100k_base")
tokenizer = lambda text: enc.encode(text,disallowed_special=())
embed_model = OpenAIEmbedding()
embed_model._tokenizer = tokenizer
node_parser = SimpleNodeParser(text_splitter=TokenTextSplitter(disallowed_special=()))
service_context = ServiceContext.from_defaults(
    embed_model=embed_model, node_parser=node_parser
)

vector_index = None
def index_pdf_documents():
    # Initialize SimpleDirectoryReader, GPTListIndex, and GPTSimpleVectorIndex
    document_reader = SimpleDirectoryReader(UPLOAD_FOLDER).load_data()
    vector_index = GPTVectorStoreIndex.from_documents(document_reader, service_context=service_context)
    print(document_reader)
    return vector_index

def search_documents(query_text, vector_index=index_pdf_documents()):
    print(vector_index)
    query_engine = vector_index.as_query_engine()
    print("Query engine:", query_engine)
    results = query_engine.query(query_text)
    print("Search results:", results)
    return results

messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}
    ]

def generate_response(user_input):
    
    # Search documents using llama_index
    print("Search user input:", user_input)
    query = user_input[0][0]
    print("Search query:", query)
    search_results = search_documents(query,index_pdf_documents())
    print("Search results:", search_results)
    print("Type of Search results:", type(search_results))

    # If search results are found, use the top result for the API call
    if search_results.response is not None:
        try:
            top_result = search_results[0]
        except:
            top_result = search_results
        print("Top result:", top_result)
        print("Top result Type :",type(top_result.response))
        messages.append({"role": "assistant", "content": top_result.response})
        return top_result.response
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print("Response:", response)
        response_text = response.choices[0].message.content
        
        messages.append({"role": "assistant", "content": response_text})
        return response_text