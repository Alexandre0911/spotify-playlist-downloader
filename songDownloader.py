from youtube_search import YoutubeSearch
import spotifyScraper
from pytube import YouTube



def downloadFile(songName: str, downloadsFolder: str) -> str:

    results = YoutubeSearch(songName, max_results=1).to_dict()
    youtubeVideoID = results[0]['id']

    downloadsFolder = downloadsFolder.replace("/", "\\")

    yt = YouTube(f"https://www.youtube.com/watch?v={youtubeVideoID}")
    video = yt.streams.filter().get_audio_only()

    video.download(filename=f"{songName}.mp4", output_path=downloadsFolder)

    return f"| {songName} | has been successfully downloaded.", downloadsFolder



def readPlaylistFile(playlistUrl: str):
    try:
        playlistID = spotifyScraper.getPlaylistInfo(playlistUrl)[1]
        playlistName = spotifyScraper.getPlaylistInfo(playlistUrl)[2]
    
        playlistFile = open(f"playlists\\{playlistName}-{playlistID}.txt", "r+")

        for line in playlistFile.readlines():
            linebreak = line.find("\n")

            if linebreak != -1:
                line = line[0:linebreak]

            try:
                result = downloadFile(line, f"C:\\Users\\vampi\\Music\\{playlistName}-{playlistID}\\")
                #print(result[0])
                downloadsFolder = result[1]
            except:
                print(f"\nThere Was An Error And The Song {line} Could Not Be Downloaded!\n")
    
        return f"All Songs Downloaded To '{downloadsFolder}'."
    except:
        return f"No Song Was Downloaded."



if __name__ == "__main__":
    print(readPlaylistFile("https://open.spotify.com/playlist/3Hr83CaveaocWG6jsFUthZ?si=f699c857a1684b5a"))
