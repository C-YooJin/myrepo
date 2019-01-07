import re
import sys


pattern = r'<contents>([.\s\S]*?)</contents>'

def save_body(file):
    with open(file) as f:
        matches = re.findall(pattern, f.read())
        with open(file+'.output', 'a') as w:
            for match in matches:
                w.write(match+'\n')


if __name__ == '__main__':
    file = sys.argv[1]
    save_body(file)
