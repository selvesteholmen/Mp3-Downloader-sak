import yt_dlp
import spotify_finder

def search_youtube(search, filter_keywords=None):
    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch",
        "noplaylist": True,
        "limit": 10,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{search}", download=False)
        if result and "entries" in result:
            for entry in result["entries"]:
                title = entry.get("title", "").lower()
                if filter_keywords:
                    if any(keyword.lower() in title for keyword in filter_keywords):
                        return entry.get("url") or entry.get("webpage_url")
                else:
                    return entry.get("url") or entry.get("webpage_url")
        return None

def find_song(song_search):
    search = spotify_finder.search_spotify(song_search)
    formatted_search = f"{search['song_name']} {search['artist_name']} {search['album_name']}"
    keywords = formatted_search.split()
    return search_youtube(formatted_search, filter_keywords=keywords)
