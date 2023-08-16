import os

import openai
from dotenv import load_dotenv
from openai.error import APIError as OPENAIError

from logger import logger

load_dotenv()

logger = logger(__name__)

openai.api_keyos = os.getenv("OPENAI_API_KEY")


def transcribe_audio(audio_file_path, model, out_dir):
    """
    Transcribes the audio file using the specified model and saves the transcription to the output directory.

    Args:
        audio_file_path (str): The path to the audio file.
        model (str): The model to use for transcription.
        out_dir (str): The output directory to save the transcription.

    Returns:
        str: The transcription text, or None if an error occurred.
    """

    logger.log("Transcribing audio...")

    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai.Audio.transcribe(model, audio_file)

            with open(out_dir, "a") as file:
                file.write(transcription["text"])

        return transcription["text"]

    except (FileNotFoundError, PermissionError, OPENAIError) as e:
        logger.error(f"Error occurred while transcribing audio: {e}")
        return None

    finally:
        logger.log("Audio transcription complete.")
        audio_file.close()


CONFIG = {
    "model_name": "gpt-4",
    "temperature": 0.1,
}


def extract_info(transcription="", instruction="", model_name="gpt-4", temperature=0.1):
    """
    Extracts information using OpenAI ChatCompletion API.

    Args:
        transcription (str): The user's transcription.
        instruction (str): The system's instruction.
        model_name (str): The name of the model to use.
        temperature (float): The temperature parameter for generating responses.

    Returns:
        str: The extracted information.
    """
    logger.log("Extracting information...")
    try:
        if not transcription or not instruction:
            raise ValueError(
                "Both 'transcription' and 'instruction' must be provided and not empty."
            )

        response = openai.ChatCompletion.create(
            model=model_name,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": instruction,
                },
                {"role": "user", "content": transcription},
            ],
            max_tokens=150,
        )

        extracted_info = response["choices"][0]["message"].get("content")
        logger.log("Information extracted successfully.")
        return extracted_info

    except (ValueError, openai.error.APIError) as e:
        logger.error(f"Error accessing OpenAI API: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected data type: {e}")
        return None
