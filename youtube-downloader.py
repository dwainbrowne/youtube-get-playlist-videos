import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pytube import YouTube


# replace with your actual video URL and output directory
output_path = '\Dwain_nas\videos\_TUTORIALS\MOBILE\FIREBASE'

def download_video(video_url, output_path):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4', res='720p').first()
    
    if stream is not None:
        print(f'Downloading: {video_url}')
        stream.download(output_path)
        print('Download completed!!')
    else:
        print(f'No 720p mp4 available for: {video_url}')



def get_all_video_in_playlist(playlist_id):
    load_dotenv() # load environment variables from .env file
    api_key = os.getenv('YOUTUBE_DATA_API_KEY') # get the API key from the environment variable

    if not api_key:
        raise Exception('The environment variable YOUTUBE_DATA_API_KEY is not set')

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.playlistItems().list(
        part='snippet',
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()

    while response:
        items = response['items']
        for item in items:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
          
            download_video(video_url, output_path)  # download video
            print(video_url)

        # check if there are more videos in the playlist than the max_results
        if 'nextPageToken' in response:
            request = youtube.playlistItems().list(
                part='snippet',
                maxResults=50,
                playlistId=playlist_id,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            response = None







# replace this with your own YouTube playlist ID
playlist_id = 'PL4cUxeGkcC9jERUGvbudErNCeSZHWUVlb'
get_all_video_in_playlist(playlist_id)
