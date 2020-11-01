#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 18:28:52 2020

@author: berikohen
"""

#%%
import os
import json
from PIL import Image
import requests
from io import BytesIO
#%%
dir_name = '/Users/berikohen/Desktop/CS-230-Project/street2shop' # From the current directory
url_dict = {}
with open(os.path.join(dir_name, 'photos.txt')) as f:
    for line in f:
        cur_line = line.split(",")
        url_dict[int(cur_line[0])] = cur_line[1][:-1]
    
#%%
with open(os.path.join(dir_name, 'train_pairs_tops.json')) as f:
    street_list = json.load(f)
#%%
with open(os.path.join(dir_name, 'retrieval_tops.json')) as f:
    product_list = json.load(f)
#%%
product_dict = {}
for pair in product_list:
    product_dict[pair['product']] = pair['photo']

#%%
pair_list = []
counter = 0
error_counter = 0
for info in street_list:
    photo_id = info['photo']
    user_image_response = requests.get(url_dict[photo_id])
    user_image = Image.open(BytesIO(user_image_response.content))
    box = info['bbox']
    cropped_user_image = user_image.crop((box['left'], box['top'], box['left'] + box['width'], box['top'] + box['height']))
    shop_image_id = product_dict[info['product']]
    shop_image_response = requests.get(url_dict[shop_image_id])
    try:
        shop_image = Image.open(BytesIO(shop_image_response.content))
        pair_list.append((cropped_user_image, shop_image))
    except: 
        error_counter += 1
    counter += 1
    print(counter)
    print(error_counter)
