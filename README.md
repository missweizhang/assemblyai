# assemblyai
audio transcript

make sure to add a `.env` file with the `ASSEMBLYAI_API_KEY` variable defined

```
ASSEMBLYAI_API_KEY=12793427580934576926037593475
```


Audio transcription for one file:
> python3 get_audio_transcript.py ~/Downloads/一颗单纯的心.mp3

Audio transcription for all the files in a folder
> python3 get_all_transcript.py -i ~/Downloads/中国史
