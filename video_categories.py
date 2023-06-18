#import libraries
import os
from time import time
from time import sleep

import googleapiclient.discovery
import googleapiclient.errors

import pandas as pd

import creds

#constants
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CSV_PATH = 'C:/Users/kevoi/OneDrive/Desktop/data-science-in-progress/youtube_categories.csv'

#main function
def category_api_runner():
    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, developerKey=creds.API_KEY)

    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()
    
    df_list = []
    for category in response['items']:
        df_dict = {
            'category_id' : category['id'],
            'category_title' : category['snippet']['title']
        }
        df_list.append(df_dict)
    category_df = pd.DataFrame(df_list)
    category_df.to_csv(CSV_PATH, header = 'column_names', index = False)

if __name__ == "__main__":
    category_api_runner()
