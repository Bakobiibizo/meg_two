import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.langchain_services.vectorstore.chroma import ChromaDB

def testing_vectorstore():
    print("- Testing ChromaDB")
    db = ChromaDB()
    db.add_text_document(file_path="docs/testing.txt")
#    db.add_mutable_document(page_content=text, document_id="test", page=0)
#    db.update_mutable_document(page_content=text, document_id="test", page=0)
    result = db.retrive_documents(query="pull the testing docs")
    print(f"-- Result: \n{result}")
    return result

if __name__ == "__main__":
    testing_vectorstore()