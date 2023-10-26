from sys import argv
import csv
import urllib.parse, urllib.request
import json
from time import sleep
import requests
import os

# Checking if the command is correct
if len(argv) > 1 and argv[1]:
    pass
else:
    print('\nCommand usage:\npython3 convertsongs.py yourplaylist.csv\nMore info at https://github.com/therealmarius/Spotify-2-AppleMusic')
    exit()

# Getting user's data for the connection
token = input("\nPlease enter your Apple Music Authorization (Bearer token):\n")
media_user_token = input("\nPlease enter your media user token:\n")
cookies = input("\nPlease enter your cookies:\n")
playlist_identifier = input("\nPlease enter the playlist identifier:\n")

# Function to get the iTunes ID of a song
def get_itunes_id(title, artist, album):
    BASE_URL = "https://itunes.apple.com/search?country=FR&media=music&entity=song&limit=5&term="
    # Search the iTunes catalog for a song
    try:
        # Search for the title + artist + album
        url = BASE_URL + urllib.parse.quote(title + " " + artist + " " + album)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        # If no result, search for the title + artist
        if data['resultCount'] == 0:
            url = BASE_URL + urllib.parse.quote(title + " " + artist)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            # If no result, search for the title + album
            if data['resultCount'] == 0:
                url = BASE_URL + urllib.parse.quote(title + " " + album)
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                data = json.loads(response.read().decode('utf-8'))
                # If no result, search for the title
                if data['resultCount'] == 0:
                    url = BASE_URL + urllib.parse.quote(title)
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request)
                    data = json.loads(response.read().decode('utf-8'))
    except:
        return print("An error occured with the request.")
    
    # Try to match the song with the results
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        for each in data['results']:
            #Trying to match with the exact track name, the artist name and the album name
            if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']           
            #Trying to match with the exact track name and the artist name
            elif each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower():
                return each['trackId']
            #Trying to match with the exact track name and the album name
            elif each['trackName'].lower() == title.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
            #Trying to match with the exact track name and the artist name, in the case artist name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["artistName"].lower() in artist.lower() or artist.lower() in each["artistName"].lower()):
                return each['trackId']
            #Trying to match with the exact track name and the album name, in the case album name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["collectionName"].lower() in album.lower() or album.lower() in each["collectionName"].lower()):
                return each['trackId']  
            #Trying to match with the exact track name
            elif each['trackName'].lower() == title.lower():
                return each['trackId']        
            #Trying to match with the track name, in the case track name are different between Spotify and Apple Music
            elif title.lower() in each['trackName'] or each['trackName'].lower() in title.lower():
                return each['trackId']
        try:
            #If no result, return the first result
            return data['results'][0]['trackId']
        except:
            #If no result, return None
            return None
    except:
        #The error is handled later in the code
        return None

# Function to add a song to a playlist
def add_song_to_playlist(session, song_id, playlist_id, playlist_name):
    try:    
        request = session.post(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks", json={"data":[{"id":f"{song_id}","type":"songs"}]})
        # Checking if the request is successful
        if requests.codes.ok:
            print(f"Song {song_id} added to playlist {playlist_name}!")
            return True
        # If not, print the error code
        else: 
            print(f"Error {request.status_code} while adding song {song_id} to playlist {playlist_name}!")
            return False
    except:
        print(f"HOST ERROR: Apple Music might have blocked the connection during the add of {song_id} to playlist {playlist_name}!\nPlease wait a few minutes and try again.\nIf the problem persists, please contact the developer.")
        return False

# Opening session
with requests.Session() as s:
    s.headers.update({"Authorization": f"{token}",
                    "media-user-token": f"{media_user_token}",
                    "Cookie": f"{cookies}",
                    "Host": "amp-api.music.apple.com",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Referer": "https://music.apple.com/",
                    "Origin": "https://music.apple.com",
                    "Content-Length": "45",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "TE": "trailers"})
    
    # Getting the playlist name
    playlist_name = os.path.basename(argv[1])
    playlist_name = playlist_name.split('.')
    playlist_name = playlist_name[0]
    
    # Opening the inputed CSV file
    with open(str(argv[1]), encoding='utf-8') as file:
        file = csv.reader(file)
        next(file)
        # Initializing variables for the stats
        n = 0
        converted = 0
        failed = 0
        # Looping through the CSV file
        for row in file:
            n += 1
            # Trying to get the iTunes ID of the song
            title, artist, album =  row[1], row[3], row[5]
            track_id = get_itunes_id(title, artist, album)
            # If the song is found, add it to the playlist
            if track_id:
                print(f'\nN°{n} | {title} | {artist} | {album} => {track_id}')
                sleep(0.5)
                if add_song_to_playlist(s, track_id, playlist_identifier, playlist_name):
                    converted += 1
                else:
                    failed += 1
            # If not, write it in a file
            else:
                print(f'N°{n} | {title} | {artist} | {album} => NOT FOUND')
                with open(f'{playlist_name}_noresult.txt', 'a+') as f:
                    f.write(f'{title} | {artist} | {album} => NOT FOUND')
                    f.write('\n')
                failed += 1
            sleep(1.5)

# Printing the stats report
print(f'\n - STAT REPORT -\nPlaylist Songs: {n}\nConverted Songs: {converted}\nFailed Songs: {failed}\nPlaylist converted at {round(converted/n*100)}%')

# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic