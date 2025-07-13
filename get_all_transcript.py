## Version 2

# audio transcript for all files in a directory
# > python3 get_all_transcript.py -i ~/Downloads/中国史

# audio transcription: speech to text
# > python3 get_audio_transcript.py ~/Downloads/一颗单纯的心.mp3

# subtitle generation: speech to text
# > python3 get_audio_transcript.py ~/Downloads/file.mp3 --subtitles

import assemblyai as aai
import sys
import os
from dotenv import load_dotenv
import argparse

def file_exists(filename):
    """Check if a file exists."""
    if os.path.exists(filename):
        user_input = input(f"File '{filename}' already exists. Overwrite? (y/n): ")

        if user_input.lower() == 'n':
            for i in range(1, 100):
                filename = os.path.splitext(audio_file_path)[0] + "_" + str(i) + ".txt"
                if not os.path.exists(filename):
                    break
        elif user_input.lower() != 'y':
            print("Invalid input. Please enter 'y' or 'n'.")
            print("Transcription cancelled.")
            return filename

    return filename


def transcribe_audio(audio_file_path, use_subtitles):
    """Transcribes a single audio file."""
    load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
    config = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber(config=config)

    try:
        transcript = transcriber.transcribe(audio_file_path)

        if use_subtitles:
            print(transcript.export_subtitles_srt())
        else:
            transcript_filename = os.path.splitext(audio_file_path)[0] + ".txt"
            transcript_filename = file_exists(transcript_filename)

            with open(transcript_filename, "w") as f:
                f.write(transcript.text)
            print(f"Transcription saved to '{transcript_filename}'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def transcribe_interactive(audio_file_path, use_subtitles, interactive):
    """Prompts the user before transcribing each audio file."""
    if interactive:
        response = input(f"Transcribe '{audio_file_path}'? (y/n): ")
        if response.lower() == 'y':
            transcribe_audio(audio_file_path, use_subtitles)
    else:
        transcribe_audio(audio_file_path, use_subtitles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio files using AssemblyAI.")
    parser.add_argument("path", help="Path to an audio file or a directory containing audio files.")
    parser.add_argument("-s", "--subtitles", action="store_true", help="Generate subtitles in SRT format.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Prompt before processing each file.")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        transcribe_interactive(args.path, args.subtitles, args.interactive)
    elif os.path.isdir(args.path):
        for filename in os.listdir(args.path):
            audio_file_path = os.path.join(args.path, filename)
            transcribe_interactive(audio_file_path, args.subtitles, args.interactive)
    else:
        print("Invalid path. Please provide a valid file or directory.")
        sys.exit(1)
