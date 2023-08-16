import os
from pathlib import Path
from typing import List, Iterable
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from logger import logger

logger = logger


class AudioProcessor:
    """

    Class AudioProcessor

    This class provides methods for processing audio files.

    Attributes:
        - dir_path: A string representing the directory path where the audio files are located.
        - out_dir: A string representing the output directory where processed files will be saved.
        - audio_suffixes: A set of strings representing supported audio file suffixes.
        - video_suffixes: A set of strings representing supported video file suffixes.
        - file_path_s: A list of strings representing the paths of audio files to be processed.
        - done_video: A boolean indicating whether a video file has been converted to audio.

    Methods: - __init__(dir_path: str, out_dir: str): Initializes the AudioProcessor object. - collect__file_path_s(
    suffixes: set[str]) -> object: Collects the file paths of supported file types. - check_file_types(files) ->
    List[str]: Checks the file types and converts video files to audio files if necessary. - video_to_mp3(
    file_path_s: List[str]) -> List[str]: Converts video files to audio files in .mp3 format. - get_file_path_s(
    file_path_s: str = None) -> List[str]: Returns the list of file paths to be processed. - segment_audio(
    audio_file_path_s: str, min_silence_len: int, silence_thresh: int) -> Iterable[AudioSegment]: Segments audio
    files based on silence detection. - check_file_length(file_s: Iterable[str], min_silence_len: int,
    silence_thresh: int) -> List[AudioSegment]: Checks the length of audio files and segments them into smaller
    chunks if necessary.

    """

    video_suffixes: set[str]

    def __init__(self, dir_path, out_dir):
        logger.info(f"Audio Processor Initialized: {dir_path}")
        self.path_file_s = Path(dir_path).resolve()
        self.out_dir = out_dir
        self.dir_path = dir_path
        self.audio_suffixes = {".mp3", ".wav"}
        self.video_suffixes = {".mp4", ".mkv"}
        self.file_path_s = []
        self.done_video = False

    def collect__file_path_s(self, suffixes: set[str]) -> List[str]:
        logger.info(f"Collecting file paths: {self.dir_path}")
        try:
            file_paths = [
                str(file)
                for file in self.path_file_s.glob("**/*")
                if file.suffix in suffixes
            ]
            return file_paths
        except OSError as e:
            logger.error(f"Error accessing directory: {self.dir_path}")
            logger.exception(e)
            raise e

    def check_file_types(self, files):
        file = ""
        logger.info(f"Checking file types: {files}")
        file_path_s = []

        unsupported_files = [
            file
            for file in files
            if not file.endswith(tuple(self.audio_suffixes.union(self.video_suffixes)))
        ]
        if unsupported_files:
            logger.error(f"File type not supported: {unsupported_files}")
            return unsupported_files

        if any(
            file.endswith(suffix)
            for suffix in self.video_suffixes
            if not self.done_video
        ):
            logger.error(f"File type not supported: {files}")
            return "File type not supported. Supported file types are: {}".format(
                self.audio_suffixes.union(self.video_suffixes)
            )

        audio_files = [
            file for file in files if file.endswith(tuple(self.audio_suffixes))
        ]
        video_files = [
            file for file in files if file.endswith(tuple(self.video_suffixes))
        ]

        if video_files:
            audio_files += self.video_to_mp3(video_files)

        file_path_s += audio_files

        for file in file_path_s:
            try:
                if any(
                    file.endswith(suffix)
                    for suffix in self.video_suffixes
                    if not self.done_video
                ):
                    logger.error(f"File type not supported: {files}")
                    return (
                        "File type not supported. Supported file types are: {}".format(
                            self.audio_suffixes.union(self.video_suffixes)
                        )
                    )
            except Exception as e:
                logger.error(f"Error: {e}")

        return file_path_s

    def video_to_mp3(self, file_path_s) -> List[str]:
        logger.info(f"Converting video to audio: {file_path_s}")
        audio_file_path_s: list[str | None] = []
        audio_file_path = None
        for file in file_path_s:
            try:
                video = AudioSegment.from_file(file)
                audio_file_path = f"{os.path.splitext(file)[0]}.mp3"
                video.write_audiofile(audio_file_path)
                self.done_video = True
            except (FileNotFoundError, TypeError, OSError) as e:
                logger.error(
                    f"Error: {e}\nThere was an issue converting the video to audio."
                )
            audio_file_path_s.append(audio_file_path)
        return audio_file_path_s

    def get_file_path_s(self, file_path_s: str = None):
        """
        @param file_path_s: A string representing the file path. If None, the method will collect file paths based
        on video and audio suffixes. @return: A list of strings representing the file paths.
        """
        logger.info(f"Getting file path: {file_path_s}")
        if file_path_s is None:
            file_path_s = self.collect__file_path_s(self.video_suffixes)
        if file_path_s is None:
            file_path_s = self.collect__file_path_s(self.audio_suffixes)
        file_path_s = self.check_file_types(file_path_s)
        self.file_path_s = self.check_file_length(file_path_s)
        return self.file_path_s

    def segment_audio(self, audio_file_path_s, min_silence_len=500, silence_thresh=-32):
        logger.info(f"Segmenting audio: {audio_file_path_s}")
        if not audio_file_path_s:
            audio_file_path_s = self.file_path_s

        if not os.path.isfile(audio_file_path_s):
            raise FileNotFoundError(f"File not found: {audio_file_path_s}")

        audio = AudioSegment.from_file(audio_file_path_s)
        detected_silence = detect_nonsilent(
            audio_file_path_s, min_silence_len, silence_thresh
        )
        if detected_silence:
            for start, end in detected_silence:
                try:
                    segment = audio[start:end]
                    if len(segment) > 0:
                        yield segment
                except Exception as e:
                    logger.error(
                        f"Error: {e}\nThere was an issue segmenting the audio."
                    )

    def check_file_length(
        self,
        file_s: Iterable[str],
        min_silence_len: int = 500,
        silence_thresh: int = -32,
    ):
        audio_chunk_s = []
        logger.info(f"Checking file length: {file_s}")
        for file in file_s:
            if os.path.getsize(file) > 256 * 128 * 10:
                file_s = self.segment_audio(file, min_silence_len, silence_thresh)
        for file in file_s:
            audio_chunk_s.append(file)
        return audio_chunk_s
