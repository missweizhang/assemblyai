## Version 1

# audio transcription: speech to text
# > python3 get_audio_transcript.py ~/Downloads/一颗单纯的心.mp3

# subtitle generation: speech to text
# > python3 get_audio_transcript.py ~/Downloads/file.mp3 --subtitles

import assemblyai as aai
import sys
import os
from dotenv import load_dotenv

# Check if the correct number of arguments is provided
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python3 get_audio_transcript.py <path_to_audio_file> [--subtitles]")
    sys.exit(1)

# Get the file path from command line argument
audio_file_path = sys.argv[1]

# Check if the --subtitles flag is present
use_subtitles = "--subtitles" in sys.argv

# Set up AssemblyAI
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
config = aai.TranscriptionConfig(language_detection=True)

transcriber = aai.Transcriber(config=config)

# transcriber = aai.Transcriber()

try:
    # Transcribe the local audio file
    # print(audio_file_path)
    transcript = transcriber.transcribe(audio_file_path)

    if use_subtitles:
        print(transcript.export_subtitles_srt())
    else:
        import os
        transcript_filename = os.path.splitext(audio_file_path)[0] + ".txt"

        if os.path.exists(transcript_filename):
            user_input = input(f"File '{transcript_filename}' already exists. Overwrite? (y/n): ")
            if user_input.lower() == 'n':
              for i in range(1, 100):
                transcript_filename = os.path.splitext(audio_file_path)[0] + "_" + i + ".txt"
                if os.path.exists(transcript_filename) == False:
                  break
            elif user_input.lower() != 'y':
                print("Invalid input. Please enter 'y' or 'n'.")
                print("Transcription cancelled.")
                sys.exit(0)

        with open(transcript_filename, "w") as f:
            f.write(transcript.text)
        print(f"Transcription saved to '{transcript_filename}'")

except Exception as e:
    print(f"An error occurred: {str(e)}")
