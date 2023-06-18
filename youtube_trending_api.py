#import libraries
import os
from time import time
from time import sleep

import googleapiclient.discovery
import googleapiclient.errors

import pandas as pd
from datetime import datetime

import creds

#constants
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CSV_PATH = 'C:/Users/kevoi/OneDrive/Desktop/data-science-in-progress/youtube_data.csv'

#api call
def api_runner():
    youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey = creds.API_KEY)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="US",
        maxResults = 10000
        )
    response = request.execute()
    #getting relevant info for each video into a dataframe
    df = pd.DataFrame(columns=['published_at', 'video_id', 'channel_id', 'title', 'channel_title', 'view_count', 'like_count', 'comment_count', 'tags', 'duration', 'category_id'])
    df_list = list()
    for video in response['items']:
        if ((video['kind'] == 'youtube#video') and (video['statistics'].get('likeCount') != None) and (video['statistics'].get('commentCount') != None) and (video['snippet'].get('tags') != None)):
        #getting info
            published_at = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', ''))
            video_id = video['id']
            channel_id = video['snippet']['channelId']
            title = video['snippet']['title']
            channel_title = video['snippet']['channelTitle']
            view_count = video['statistics']['viewCount']
            like_count = video['statistics']['likeCount']
            comment_count = video['statistics']['commentCount']
            tags = video['snippet']['tags']
            duration = pd.to_timedelta(video['contentDetails']['duration']).total_seconds() / 60 #duration in minutes
            category_id = video['snippet']['categoryId']


        #adding putting info into dictionary
            row = {
                'published_at' : published_at,
                'video_id' : video_id,
                'channel_id' : channel_id,
                'title' : title,
                'channel_title' : channel_title,
                'view_count' : view_count,
                'like_count' : like_count,
                'comment_count' : comment_count,
                'tags' : tags,
                'duration' : duration,
                'category_id' : category_id
            }
        #appending dictionary to list
            df_list.append(row)

    #converting list of dictionaries to dataframe        
    df = pd.DataFrame(df_list)
    df['timestamp'] = pd.Timestamp.now()

    if not os.path.isfile(CSV_PATH):
        df.to_csv(CSV_PATH, header = 'column_names', index = False)
    else:
        df.to_csv(CSV_PATH, mode = 'a', header = False, index = False)

if __name__ == '__main__':
    api_runner()
    print('API ran successfully')
