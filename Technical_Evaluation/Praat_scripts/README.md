# Praat Scripts for Technical Evaluation
Necessary Praat Scripts 
(*You need Praat on your computer to run .praat scripts*)

## How to run
Put the script in the directory that contains .wav or .mp3 files and run it.

## Script Description
### Script 'test_silence_detection.praat' will 
1. Convert .wav or .mp3 files to single channel .wav format.
2. Label silent / voiced sections of each file.
3. Save the result as a TextGrid file.

### Script 'pitch_detection.praat' will
1. Get all mono .wav file in the directory and check their pitch.
2. Section with 'beep' sounds will be marked with high scores.
3. Save the result as a Pitch file. (readable in TextEditor)
