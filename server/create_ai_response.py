from interfaces import AIResponse, Content, Usage
from uuid import uuid4
from datetime import datetime

class CreateAIResponse():
    def __init__(self):
        pass

    def create(self, ai_response, mode):
        if mode == "image":
            content = Content(imageUrl=ai_response.data[0].url)
            usage = Usage(prompt_tokens=0, completion_tokens=1000, total_tokens=1000)
            response = AIResponse(
                id=str(uuid4()),
                mode="image",
                role="assistant",
                object="image.create",
                created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                content=content.__dict__,
                usage=usage.__dict__,
                viewerContent=True
            )
            res = response.__dict__
            print(f"-- Created Response: \n{res}")
            return res
        elif mode == "text":
            content = Content(text=ai_response.generations[0][0].text)
            usage = Usage(
                prompt_tokens=ai_response.llm_output["token_usage"]["prompt_tokens"],
                completion_tokens=ai_response.llm_output["token_usage"]["completion_tokens"],
                total_tokens=ai_response.llm_output["token_usage"]["total_tokens"],
            )
            response = AIResponse(
                viewerContent=False,
                id=str(uuid4()),
                mode="text",
                role="assistant",
                object="chat.completion",
                created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                content=content.__dict__,
                usage=usage.__dict__
            )
            res = response.__dict__
            print(f"-- Created Response: \n{res}")
            return res
