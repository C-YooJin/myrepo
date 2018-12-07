import sys
import os
import json
import time
import base64

LOG_TERM = 10000
MAX_LINE = 0
LANG = ['en', 'zh', 'ko', 'ja', 'in']

def store(data, filepath):
    with open(filepath, 'a') as f:
        try:
            if data['in_reply_to_status_id_str'] !='None':
                f.write('\t'.join([
                    data['id_str'],
                    data['in_reply_to_status_id_str'],
                    data['text'],
                    data['created_at'],
                    data['user']['id_str'],
                    data['lang']
                ]))
                f.write('\n')
        except:
            pass
           # with open('error_log.txt', 'a') as e:
            #    e.write(data)

def filter(data):
    try:
        data = json.loads(base64.b64decode(data['contentMap']['syndiContentRaw']['data']).decode('utf-8'))
    except:
        with open('errorlog.txt', 'a') as f:
            f.write(data)   
    return data

def store_by_lang(data, output_dir):
    if data['lang'] in LANG:
        store(data, output_dir + '/' + data['lang'] + '.tsv')


def cleanup(data):
    data['in_reply_to_status_id_str'] = str(data['in_reply_to_status_id_str'])
    data['text'] = '\\n'.join(data['text'].replace('\t', '\\t').split('\n'))
    return data


def reduce(filepath, output_dir):
    total = 1

    with open(filepath) as f:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for line in f:
            data = json.loads(line)
            try:
                data = filter(data)
                data = cleanup(data)
                store_by_lang(data, output_dir)

                if total % LOG_TERM == 0:
                    print('Parsed tweets: {}'.format(total))

                if total == MAX_LINE:
                    break

                total += 1

            except:
                pass
                #with open('error_log.txt', 'a') as e:
                 #   e.write(line)


if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) == 3:
        print('Start reducing...: ' + sys.argv[1])
        reduce(sys.argv[1], sys.argv[2])
        elapsed_time = time.time() - start_time
        print(time.strftime("Elapsed time: %H:%M:%S", time.gmtime(elapsed_time)))

    else:
        print('Usage: reduce_tweet.py SOURCE.TSV OUTPUT_DIR')

