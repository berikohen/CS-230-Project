#%% Import Packages
import os
import json
from PIL import Image

#%% Process annotation files and store the photo
# id and bounding box of each item
user_dict = {}
shop_dict = {}
json_directory = '/Users/berikohen/Desktop/validation/annos'
for filename in os.listdir(json_directory):
    with open(json_directory + '/' + filename) as f:
        cur_json = json.load(f)
        if cur_json['source'] == 'user':
            n_items = len(cur_json) - 2
            pair_id = cur_json['pair_id']
            file_number = filename[0:filename.find('.')]
            if pair_id not in user_dict:
                user_dict[pair_id] = []
            for i in range(n_items):
                key = 'item' + str(i+1)
                user_dict[pair_id].append((file_number,cur_json[key]['bounding_box']))
        else:
            n_items = len(cur_json) - 2
            pair_id = cur_json['pair_id']
            file_number = filename[0:filename.find('.')]
            if pair_id not in shop_dict:
                shop_dict[pair_id] = []
            for i in range(n_items):
                key = 'item' + str(i+1)
                shop_dict[pair_id].append((file_number,cur_json[key]['bounding_box']))
#%% Upload images and store with their photo number
image_directory = '/Users/berikohen/Desktop/validation/image'
image_dict = {}
counter = 0
for filename in os.listdir(image_directory):
    file_number = filename[0:filename.find('.')]
    img = Image.open(image_directory + '/' + filename)
    image_dict[file_number] = img
    counter += 1
    if counter == 2000: break
    
#%% Create a list of tuples where each tuples is the bounded 
# image of a user item and the corresponding shop image
pair_list = []
for pair_id in user_dict:
    tuples = user_dict[pair_id]
    for item in tuples:
        file_number = item[0]
        box = item[1]
        if file_number in image_dict:
            image = image_dict[file_number]
            cropped = image.crop((box[0], box[1], box[2], box[3]))
            if pair_id in shop_dict:
                for item in shop_dict[pair_id]:
                    shop_number = item[0]
                    if shop_number in image_dict:
                        pair_list.append((cropped, image_dict[shop_number]))
    
        