from langchain.document_loaders import TextLoader

class DocumentLoader(TextLoader):
    def __init__(self, file_path):
        super().__init__(file_path)