from dotenv import load_dotenv
import requests
import base64
import json
import os



load_dotenv()
clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")



def getToken():
    authString = clientID + ":" + clientSecret
    authBytes = authString.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authBase64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"grant_type": "client_credentials"}

    result = requests.post(url, headers=headers, params=params)
    jsonResults = json.loads(result.content)
    token = jsonResults["access_token"]

    return token



def getAuthReader():
    return {"Authorization": "Bearer " + getToken()}



def getPlaylistInfo(playlistURL: str) -> tuple[str, str]:
    # Step 1 - Get PlaylistID
    xArg = "playlist/"
    xIndex = playlistURL.find(xArg)                 # Returns index of "p"
    yIndex = playlistURL.find("?si=")                 # Returns index of "?"

    playlistID = playlistURL[xIndex + len(xArg) : yIndex]



    # Step 2 - Get Playlist Track List
    spotifyResponse = requests.get(f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?fields=items%28track%28name%2C+artists%28name%29%29%29", headers=getAuthReader())
    jsonSpotifyResponse = json.loads(spotifyResponse.content)
    spotifyResponseName = requests.get(f"https://api.spotify.com/v1/playlists/{playlistID}?fields=name", headers=getAuthReader())
    jsonSpotifyResponseName = json.loads(spotifyResponseName.content)

    playlistName = jsonSpotifyResponseName['name']
    trackDict = jsonSpotifyResponse['items']



    # Step 3 - Write Tracks To Output File With PlaylistID As Name (format: playlistID.txt)
    outputFile = open(f"playlists\\{playlistName}-{playlistID}.txt", "w+")
    outputContent = ""
    count = 0

    for track in trackDict:
        count += 1
        trackArtists = ""
        trackName = track['track']['name']

        for i in range(len(track['track']['artists'])):
            trackArtists += track['track']['artists'][i]['name']
            if i != len(track['track']['artists']) - 1:                 # If artist is not the last artist in artistlist, append ", " for readability
                trackArtists += " "
        
        
        outputContent += f"{trackArtists} - {trackName}"
        if count != len(track['track']):                                # If song is not the last son in the playlist, append "\n" for readability
            outputContent += "\n"

    outputFile.write(outputContent)
    outputFile.close()



    # Finally, End Function Returning Success Message
    return f"\nPlaylist Scraped Successfully. Output File > {playlistID}.txt", playlistID, playlistName



if __name__ == "__main__":
    print(getPlaylistInfo("https://open.spotify.com/playlist/3Hr83CaveaocWG6jsFUthZ?si=f699c857a1684b5a")[0])
