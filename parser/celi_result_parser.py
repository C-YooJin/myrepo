import os
import re

filepath = '/Users/user/Desktop/output'
files = os.listdir(filepath)
resultpath = '/Users/user/Desktop/easyalign'

if not os.path.exists(resultpath):
    os.makedirs(resultpath)

class CeliResult:
    def __init__(self, resultpath):
        self.text = self.datareader(resultpath)
        self.groups = self.groupmaker()
        self.len = len(self.groups)

    def datareader(self, resultpath):
        with open(resultpath, 'r') as f:
            text = f.read()
        return text

    def groupmaker(self):
        #pattern = re.compile(r'<input>[.\s\w\W]+?(?=<input>)')
        pattern = re.compile(r'<input>[.\s\w\W]+?<\/clause>')
        groups = pattern.findall(self.text)
        return groups

    def __len__(self):
        return self.len

    def __iter__(self):
        return

    def __getitem__(self, item):
        return OneGroup(self.groups[item])


class OneGroup(CeliResult):
    def __init__(self, data):
        self.text = data
        self.input_text = self.getinput()
        self.phonemes = self.getphone()

    def getinput(self):
        pattern = re.compile(r'<input>([.\s\w\W]+?)<\/input>')
        input_text = pattern.findall(self.text)[0]
        return input_text

    def getphone(self):
        pattern = re.compile('phonemes=\'([\w\W.]+?)\'')
        phonemes = pattern.findall(self.text)
        phonemes_string = ' '.join(map(str, phonemes))
        return phonemes_string