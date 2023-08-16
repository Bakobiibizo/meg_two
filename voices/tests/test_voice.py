
from voice_generation import VoiceGeneration


def run_voice_generation(text, voice_id):
    voice = VoiceGeneration()
    
    voice.generate_voice(text, voice_id)


if __name__ == "__main__":
    with open("input/input.txt", "rb") as f:
        text = f.read().decode("utf-8")
    run_voice_generation(text=text, voice_id="D38z5RcWu1voky8WS1ja")