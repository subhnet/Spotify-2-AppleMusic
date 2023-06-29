from sys import argv, exit
import requests
import time

if len(argv) > 1 and argv[1]:
    pass
else:
    print('\nCommand usage:\npython3 addsongs.py yourplaylist_itunes-version.csv\nMore info at https://github.com/therealmarius/Spotify-2-AppleMusic')
    exit()

token = input("\nPlease enter your Apple Music Authorization (Bearer token):\n")
media_user_token = input("\nPlease enter your media user token:\n")
cookies = input("\nPlease enter your cookies:\n")
playlist_identifier = input("\nPlease enter the playlist identifier:\n")

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

    def add_song_to_playlist(song_id, playlist_id):
        request = s.post(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks", json={"data":[{"id":f"{song_id}","type":"songs"}]})
        if requests.codes.ok: print(f"Song {song_id} added to playlist {playlist_id}!")
        else: print(f"Error {request.status_code} while adding song {song_id} to playlist {playlist_id}!")

    with open(argv[1]) as itunes_identifiers_file:
        time.sleep(5)
        n = 0
        for line in itunes_identifiers_file:
            n += 1
            itunes_identifier = int(line)
            print(f"\nAdding song n°{n} with its iTunes identifier...")
            add_song_to_playlist(itunes_identifier, playlist_identifier)
            time.sleep(1.5)
        print(f"\nAdded {n} songs to {playlist_identifier}")

# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic