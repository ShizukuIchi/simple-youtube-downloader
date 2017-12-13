import requests
import re
import json
import sys
from urllib.parse import parse_qs

# Something like https://www.youtube.com/watch?v=XXXXXXXXXXX
url = sys.argv[1]

res = requests.get(url)
args_json_string = re.search('ytplayer.config = ({.*?});', res.text)

if len(args_json_string.groups()) is 1:
    j = json.loads(args_json_string.group(1))
else:
    print('no config found')
    sys.exit()

# Take off reserved characters from video name      
title = re.sub(r'[:<>"\\\/\|\?\*]', '',j['args']['title'])
qs = parse_qs(j['args']['url_encoded_fmt_stream_map'])
res = requests.get(qs['url'][0])
if res.status_code == 200:
    # Directly replace existing file
    with open(title+'.mp4', 'wb') as f:
        for chunk in res:
            f.write(chunk)
else:
    print('request error')