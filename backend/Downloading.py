from mp3_converter import download_youtube_audio
from spotify_to_youtube import find_song


def spotify_download(search):
    link = find_song(search)
    download_youtube_audio(link)

def youtube_download(link):
    download_youtube_audio(link)

# Example usage / debugs and tests:
#spotify_download("Head in the celing fan Title fight")
#youtube_download("https://www.youtube.com/watch?v=Z0OXRP-B200")