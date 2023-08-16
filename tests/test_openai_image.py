import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.langchain_services.openai_image import OpenAIImage

def test_openai_image():
    openai = OpenAIImage()
    prompt = "an old inn with a tree growing out of it. a duck wearing a fedora sit out front. high fantasy style, high definition, ultra realistic, 4k, unreal engine, award winning photography, masterwork, bestwork, intricate detail, clean linework"
    n = 1
    size = "512x512"
    response = openai.get_image_response(prompt = prompt, n=n, size=size)
    print(response)

if __name__ == "__main__":
    test_openai_image()