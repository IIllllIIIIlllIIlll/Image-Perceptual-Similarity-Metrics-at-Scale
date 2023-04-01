"""
Extracts only images from the 4chan /pol/ and /k/ boards from the ICWSM 2021 memes chan files.
Expects images to be fully uncompressed.
"""

import PIL
from PIL import Image
import json
from collections import defaultdict
from pprint import pprint
from itertools import islice
from pathlib import Path
from shutil import copy
from tqdm import tqdm

_4chan_json_f = "<home directory>/icwsm2021-memes-chans/track_4chan_pHashes.json"
bulk_loc = "<home directory>/icwsm2021-memes-images/uncompressed/"
filtered_loc = "<home directory>/icwsm2021-memes-images/filtered/"


with open(_4chan_json_f) as infile:
    data = json.load(infile)


chan_counter = defaultdict(int)
images_set = set()

for _superkey, _superval in data.items():
    for _key, _val in _superval.items():
        if '4chan_' in _key:
            chan = _key.split('_')[1]
            chan_counter[chan] += 1
            images_set.add(_val[0])

pprint(chan_counter)
print(len(images_set))

bulk_loc = Path(bulk_loc)
filtered_loc = Path(filtered_loc)

for img_name in tqdm(images_set):
    full_img_name = img_name + '.jpg'
    try:
        image = Image.open(bulk_loc / full_img_name).convert('RGB')
    except PIL.UnidentifiedImageError:
        print('%s does not look like an image' % full_img_name)
    else:
        copy(bulk_loc / full_img_name, filtered_loc /full_img_name)