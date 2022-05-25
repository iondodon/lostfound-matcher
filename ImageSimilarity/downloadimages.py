import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor
import json
import uuid
from tqdm import tqdm_notebook as tqdm

# Load cscv with images url
data = pd.read_csv('flipkart/flipkart_com-ecommerce_sample.csv')

#data = data.iloc[0:10,:]

def get_first_image_url(df):
    try:
        images_urls = df['image'].replace('["','').replace('"]','').split('", "')
        first_image = images_urls[0]

        return first_image
    except:
        return None

# Get all first image url
image_url = data.apply(lambda x:get_first_image_url(x), axis=1)
data['image_url'] = image_url

def get_image(uniq_id,name,category,url):
    try:
        # Image
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((250, 250), Image.ANTIALIAS)
        img.save('flipkart/images_2/images_2/{}.jpg'.format(uniq_id))
        
        # Metadata
        img_metadata = pd.DataFrame({'id': [uniq_id],
                                     'name': [name],
                                     'category': [category]})
        
        return img_metadata
    except:
        print('fail: {}'.format(url))
        pass

with ProcessPoolExecutor(max_workers = None) as executor:
    results = list(tqdm(executor.map(get_image,
                                     data.uniq_id.values,
                                     data.product_name.values,
                                     data.product_category_tree.values,
                                     data.image_url.values),
                total = len(data)))

# Create Metadata csv
metadata = pd.concat(results,axis=0)

metadata.to_csv('flipkart/metadata.csv',index=False)

def str_test(df,size):
  string = str(df.category).replace('["','').replace('>> ','').replace('"]','')
  string = string[0:size]
  return string

a = pd.DataFrame()
a['category'] = metadata['category']
a['category_2'] = a.apply(lambda x: str_test(x, 30), axis=1)

len(a.category.unique()),len(a.category_2.unique())

a.category_2.unique()