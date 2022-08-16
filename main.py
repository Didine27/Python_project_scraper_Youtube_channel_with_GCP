from urllib import response
from googleapiclient.discovery import build 
import pandas as pd 
import seaborn as sns 
import json
from yt_crowling import youtube_analyse as yt
from matplotlib import pyplot as plt


# build the youtube api 
api_key = 'PUT THE API KEY HERE' # On the Youtube DATA API v3 application on GCP you can create your API key 
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)

# add the channel_ids 

channel_ids = ['UC4VOE8jQPWUPp4PpNK8zhIg', # Pascale Boniface                   
                'UCHGMBrXUzClgjEzBMei-Jdw', #Le Dessous des Cartes - ARTE 
                'UCW2QcKZiU8aUGg4yxCIditg'] #chaine de euronews



# get video ids of ARTE
youtube_statistic = yt.channel_stat(youtube,channel_ids)
channel_analyse = yt.analyse_1(youtube_statistic)
playlist_id = channel_analyse.loc[channel_analyse["channel_name"] =="Le Dessous des Cartes - ARTE","playlist_id"].iloc[0]
videos_ids = yt.get_video_ids(youtube,playlist_id)

# get video_statistics 
videos_statistics = yt.get_videos_details(youtube,videos_ids)

# show the top most watched videos 
videos_analyse = yt.analyse_2(videos_statistics)
top_5_videos = videos_analyse.sort_values(by='views', ascending=False).head(10)
print(top_5_videos)


