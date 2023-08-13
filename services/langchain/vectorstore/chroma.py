from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from services.langchain.vectorstore.text_splitter import TextSplitter
from services.langchain.vectorstore.embeddings import Embeddings
from langchain.document_loaders import TextLoader

class ChromaDB():
    def __init__(self):
        self.chroma = Chroma()
        self.embeddings = Embeddings().embeddings
        self.persistent_directory = "/docs/chromadb"
        self.vectordb = Chroma(
            persist_directory=self.persistent_directory,
            embedding_function=self.embeddings
            )

    def add_text_document(self, file_path, collection_name="text_documents"):
        text_loader = TextLoader(file_path=file_path)
        documents = text_loader.load()
        text_splitter = TextSplitter().text_splitter
        docs = text_splitter.split_documents(documents)
        self.db = self.chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persistent_directory,
            collection_name=collection_name
            )

#    def add_mutable_document(self, page_content, document_id, page, collection_name="mutable_documents"):
#        document = Document(page_content=page_content, metadata={"page":page})
#        return self.db.from_documents(
#            documents =[document],
#            embedding=self.embeddings,
#            persist_directory=self.persistent_directory,
#            collection_name=collection_name,
#            ids=document_id
#            )
#
#    def update_mutable_document(self, page_content, document_id, page):
#        document = Document(page_content=page_content, metadata={"page":page})
#        return self.db.update_document(document, document_id)
#
    def retrive_documents(self, query):
        retriver = self.db.as_retriever(search_type="mmr")
        return retriver.get_relevant_documents(query=query)