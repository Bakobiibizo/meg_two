from logger import Logger

logger = Logger


def format_transcript():
    """
    Formats the transcript by removing leading and trailing spaces,
    and adding a newline after each sentence.

    @return: Return the number of characters written to the file.
             If a sentence contains only spaces, return None.
    """
    logger.log("Formatting transcript")
    with open("src/out/transcript.txt", "r") as file:
        raw = file.read().split(".", -1)
        for each in raw:
            cleaned = f"{each.strip()}\n"

            with open("src/out/full_transcript.txt", "a") as f:
                logger.log_info(f"Writing {cleaned} to file")
                return f.write(cleaned) if cleaned != "\n" else None
    logger.log("Transcript formatted.")


def format_minutes(minutes):
    """
    @param minutes: A dictionary containing minutes data in key-value pairs.
    @return: None

    """
    logger.log("Formatting minutes")
    human_readable_text = ""

    for key, value in minutes.items():
        human_readable_text += f"{key}: {value}\n"

    with open("src/out/minutes.txt", "w") as file:
        file.write(human_readable_text)
    logger.log("Minutes formatted.")
