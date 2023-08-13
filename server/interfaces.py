from typing import List
from datetime import datetime

class Prompt:
    def __init__(self, mode: str, model: str, prompts: List[str], imageUrl: str = None, base64Image: str = None, n: int = None, size: str = None, timestamp: datetime = None):
        self.mode = mode
        self.model = model
        self.prompts = prompts
        self.imageUrl = imageUrl
        self.base64Image = base64Image
        self.n = n
        self.size = size
        self.timestamp = timestamp

class ChatWindowMessage:
    def __init__(self, role: str, content: str, total_tokens: int):
        self.role = role
        self.content = content
        self.total_tokens = total_tokens

class Usage:
    def __init__(self, prompt_tokens:int, completion_tokens:int, total_tokens:int):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

class Content:
    def __init__(self, text:str=None, index:int=None, imageUrl:str = None, base64Image:str = None):
        self.text = text
        self.index = index
        self.imageUrl = imageUrl
        self.base64Image = base64Image

class AIResponse:
    def __init__(self, id: str, mode: str, role: str, created: str, content: Content, usage=Usage, viewerContent=bool, object: str=None):
        self.id = id
        self.mode = mode
        self.role = role
        self.object = object
        self.created = created
        self.content = content
        self.usage = usage
        self.viewerContent = viewerContent


