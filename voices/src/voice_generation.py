import os
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import loguru
import datetime

load_dotenv()

CHUNK_SIZE = 1024

logger = loguru.logger


def api_requests(voice_id, text, api_key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    payload = {
        "text": f"{text}",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Insomnia/2023.5.2",
        "Accept": "audio/mpeg",
        "xi-api-key": f"{api_key}"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None

    return response


if __name__ == "__main__":
    try:
        sound = AudioSegment.empty()
        date = datetime.date.today()
        entry = len(os.listdir("./audio/output"))
        file_path = "./audio/input/in.txt"
        audio_path = f"./audio/output/{date}-{entry}-entry.mp3".strip(".txt")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            logger.debug(text)

        response = api_requests(text=text, voice_id="XrExE9yKIg1WjnnlVkGX", api_key=os.getenv("ELEVENLABS_API_KEY"))
        if response is None:
            logger.error("API request failed. Check the error message for details.")
            exit(1)

        logger.debug(response.status_code)

        with open(audio_path, "wb") as f:
            f.write(response.content)
        play(AudioSegment.from_mp3(audio_path))
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        raise

