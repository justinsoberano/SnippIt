from googleapiclient.discovery import build
from pytube import YouTube
from pydub import AudioSegment
import os

API_KEY = "Your API Key Goes Here"

def urlCreator():
    print("Welcome to SnippIt: Song Snippet Maker")
    songName = input("Song name: ")
    artistName = input("Artist name: ")
    
    # Creates the search query used for the YouTube API
    searchQuery = songName + " " + artistName + " audio"
    
    # Creates the YouTube API
    youtube = build(
        'youtube',
        'v3',
        developerKey = API_KEY
    )
    
    # Make request to the YouTube API
    request = youtube.search().list(
        part = 'snippet',
        maxResults = 1,
        q = searchQuery,
    )
    
    response = request.execute()
    
    #Grabs the video ID from the JSON response, needed for the next request
    videoID = response['items'][0]['id']['videoId']

    url = "https://www.youtube.com/watch?v=" + videoID
    return url

def mp4Downloader():
    url = urlCreator()
    video_object = YouTube(url)
    base_dir = downloadFolder()

    # Grabs highest quality of audio available and defaults to mp4
    song = video_object.streams.get_audio_only()
    
    try:
        song.download(downloadFolder())    
        sound = AudioSegment.from_file(os.path.join(base_dir, song.title + ".mp4"))
        
        print(song.title + " successfully loaded.")
        
        beginTime = input("Where would you like the song snippet to begin? (mm:ss) || ")
        EndTime = input("Where would you like the song snippet to end? (mm:ss) || ")
    
        startTime = beginTime.split(":")
        EndTime = EndTime.split(":")
    
        start = ((60 * int(startTime[0])) + int(startTime[1])) * 1000
        end = ((60 * int(EndTime[0])) + int(EndTime[1])) * 1000
        
        clip = sound[start:end]
        
        clip.export(os.path.join(base_dir, song.title + ".mp4"), format="mp4")
        
        print("A snippet of " + song.title + " has been added to your downloads folder")
        
    except:
        print("SnippIt cannot load. Full song has been added to your downloads folder.")
       
def downloadFolder():
    # Checks the OS and sets the download folder accordingly
    # Windows
    if os.name == "nt":
        directory = f"{os.getenv('USERPROFILE')}\\Downloads"
    # Unix Based
    else: 
        directory = f"{os.getenv('HOME')}/Downloads"

    return directory

mp4Downloader()
