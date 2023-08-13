import os
import openai
from dotenv import load_dotenv

load_dotenv()

class OpenAIImage():
    def __init__(self):
        self.openai = openai.Image(api_key=os.getenv("OPENAI_API_KEY"))

    def get_image_response(self, prompt=None, n=1, size="256x256"):
        response = self.openai.create(prompt=prompt, n=n, size=size)
        print(f"-- Response: \n{response}")
        return response
