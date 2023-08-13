import os
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

class Embeddings():
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
