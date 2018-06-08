# Goes through all mono .wav files
# Detects 'beep' pitch in each file
# Saves pitch object as a text file

directory$ = "./"
wvs$ = directory$ + "/mono*.wav"
wavList = Create Strings as file list: "wavList", wvs$
selectObject: wavList

numFiles = Get number of strings
for fileNum from 1 to numFiles
    select Strings wavList
    fileName$ = Get string: fileNum
    sound = Read from file... 'directory$'/'fileName$'
    To Pitch: 0, 184.3, 186.8
    Save as text file: "'directory$'/" + fileName$ - ".wav" + ".Pitch"
endfor
