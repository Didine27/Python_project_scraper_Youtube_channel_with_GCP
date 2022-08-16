from urllib import response
from googleapiclient.discovery import build 
import pandas as pd 
from matplotlib import pyplot as plt
import json


# class to get statistics from a youtube video channel 

class youtube_analyse :
    def channel_stat(youtube,channel_ids):
        request = youtube.channels().list(part="snippet,contentDetails,statistics",id = channel_ids)
        extract_data = request.execute()
        statistics = []
        for i in range(0,len (extract_data["items"])):

            data =  dict (channel_name = extract_data["items"][i]["snippet"]["title"],
            Subscribers = extract_data["items"][i]["statistics"]["subscriberCount"],
            views = extract_data["items"][i]["statistics"]["viewCount"],
            videos_count = extract_data["items"][i]["statistics"]["videoCount"],
            playlist_id = extract_data["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"])
            statistics.append(data)
   
        return statistics
    



# function to analyse data 
    def analyse_1 (statistics):

        df = pd.DataFrame(statistics)
        df["Subscribers"]= pd.to_numeric(df["Subscribers"])
        df["views"]= pd.to_numeric(df["views"])
        df["videos_count"]= pd.to_numeric(df["videos_count"])
        return df 
        
        

# function to get video ids

    def get_video_ids(youtube,playlist_id):
        request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId = playlist_id, 
        maxResults = 50
        )
        response = request.execute()

        video_ids = []

        for i in range(0,len(response["items"])):

            data = response["items"][i]["contentDetails"]["videoId"]
            video_ids.append(data)
    
            next_page_token = response.get("nextPageToken")
            more_pages = True

        while more_pages:

            if next_page_token is None:
                more_pages = False

            else:
                request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId = playlist_id, 
                maxResults = 50,
                pageToken = next_page_token
                )
                response = request.execute()

                for i in range(0,len(response["items"])):
                    data = response["items"][i]["contentDetails"]["videoId"]
                    video_ids.append(data)

                    if next_page_token is None:
                        more_pages = False
                        next_page_token = response.get("nextPageToken")
            
                    return video_ids

    
# function to get video statistics 
    def get_videos_details ( youtube, video_ids):
        statistic_of_all_videos = []

        for i in range (0, len(video_ids), 50):
            request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids[i:i+50])
            )
            response = request.execute()

            for video in response["items"]:
                video_stats = dict(Title = video["snippet"]["title"],
                                Published_date = video["snippet"]["publishedAt"],
                                views = video["statistics"]["viewCount"],
                                likes = video["statistics"]["likeCount"],
                                comments = video["statistics"]["commentCount"]
                                )
                statistic_of_all_videos.append(video_stats)


            return statistic_of_all_videos
    
    
    def analyse_2 (statistic_of_all_videos):

        videos_data = pd.DataFrame(statistic_of_all_videos)
        videos_data["views"] = pd.to_numeric(videos_data["views"])
        videos_data["likes"] = pd.to_numeric(videos_data["likes"])
        videos_data["comments"] = pd.to_numeric(videos_data["comments"])
        videos_data["Published_date"] = pd.to_datetime(videos_data["Published_date"],format='%Y/%m/%d %H:%M:%S')
        return videos_data
