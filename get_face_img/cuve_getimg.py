import json
import urllib.request
import os

# change rawfilepath to your local path of raw file (downloaded from cuve)
rawfilepath = '/Users/user/Documents/image.image_precoll.20180607000000-20180607010000.00000'

# change img_download_path to your local path where you want to download the images
# program will create the directory if it doesn't exist already
img_download_dir = '/Users/user/Documents/sample_face/'
try:
    os.stat(img_download_dir)
except:
    os.mkdir(img_download_dir)

# change catname to whatever name you want for the downloaded images
# program will name the images in catname_(index) format
catname = 'faceimage'

json_data = []
for line in open(rawfilepath,'r'):
    json_data.append(json.loads(line))

with open ('/Users/user/Desktop/img_meta_match.txt', 'w') as m:
    with open('/Users/user/Desktop/sampledata_urls.txt', 'w') as f:
        for i in range(len(json_data)):
            aUrl = json_data[i]['contentMap']['hadesIndexInfo']['metaMap']['url.imageurl']
            f.write(aUrl+'\n')

            try:
                localpath = img_download_dir + '{0}_({1}).jpg'.format(catname, i)
                urllib.request.urlretrieve(aUrl, localpath)
                m.write(str(i)+'\t'+json_data[i]['uniqueKey'] + '\t'
                        + json_data[i]['contentMap']['featureFaceInfo']['metaMap']['facecnt']
                        + '\t' + aUrl + '\n')
            # if url is not found
            except:
                m.write(str(i)+'\t'+json_data[i]['uniqueKey'] + '\t'
                        + 'URL NOT VALID'
                        + '\t' + aUrl + '\n')
                print('index %d'%(i), 'url not found')