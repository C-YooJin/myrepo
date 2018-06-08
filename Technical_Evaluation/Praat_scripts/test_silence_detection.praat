clearinfo

# read files
directory$ = "./"
listfile$ = "'directory$'"+"/process_list.txt"
textfile$ = "'directory$'"+"/result.txt"
wvs$ = directory$ + "/*.wav"
mps$ = directory$ + "/*.mp3"

fileappend "'textfile$'" File names'tab$'
fileappend "'textfile$'" 'newline$'

wavList = Create Strings as file list: "wavList", wvs$
selectObject: wavList

# Make files list
numFiles = Get number of strings
for fileNum from 1 to numFiles
   select Strings wavList
   fileName$ = Get string: fileNum
   fileappend "'textfile$'" 'fileName$'
   fileappend "'textfile$'" 'newline$'
   sound = Read from file... 'directory$'/'fileName$'
   Convert to mono
   Save as WAV file: "'directory$'/" + "mono_" + fileName$ 
   selectObject: sound
   grid = To TextGrid (silences): 100, 0, -25, 1.2, 0.1, "silent", "sounding"
   selectObject: grid
   Save as text file: "'directory$'/" + fileName$ - ".wav" + "_labeled.TextGrid"
endfor


# In case there are mp3 files
mpList = Create Strings as file list: "mpList", mps$
selectObject: mpList

# Make files list
numFiles = Get number of strings
for fileNum from 1 to numFiles
   select Strings mpList
   fileName$ = Get string: fileNum
   fileappend "'textfile$'" 'fileName$'
   fileappend "'textfile$'" 'newline$'
   sound = Read from file... 'directory$'/'fileName$'
   Convert to mono
   Save as WAV file: "'directory$'/" + "mono_" + fileName$ - ".mp3" + ".wav"
   selectObject: sound
   grid = To TextGrid (silences): 100, 0, -25, 1.2, 0.1, "silent", "sounding"
   selectObject: grid
   Save as text file: "'directory$'/" + fileName$ - ".mp3" + "_labeled.TextGrid"
endfor