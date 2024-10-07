from sys import argv
import sys
import csv
import urllib.parse, urllib.request
import json
from time import sleep
import requests
import os

# Delay (in seconds) to wait between tracks (to avoid getting rate limted) - reduce at own risk
delay = 1

# Checking if the command is correct
if len(argv) > 1 and argv[1]:
    pass
else:
    print('\nCommand usage:\npython3 convertsongs.py yourplaylist.csv\nMore info at https://github.com/therealmarius/Spotify-2-AppleMusic')
    exit()

# Function to get contents of file if it exists
def get_connection_data(f,prompt):
    if os.path.exists(f):
        with open(f,'r') as file:
            return file.read().rstrip('\n')
    else:
            return input(prompt)

def create_apple_music_playlist(session, playlist_name):
    base_url = "https://amp-api.music.apple.com"
    url = f"{base_url}/v1/me/library/playlists"
    data = {
        'attributes': {
            'name': playlist_name,
            'description': '',
        }
    }

    # Helper function to get all playlists with pagination
    def get_all_playlists(session):
        playlists = []
        next_page = url  # Start with the base URL
        while next_page:
            response = session.get(next_page)
            if response.status_code == 200:
                result = response.json()
                playlists.extend(result['data'])

                # Handle the relative URL issue for pagination
                if 'next' in result and result['next']:
                    next_page = result['next']
                    if next_page.startswith('/'):
                        next_page = base_url + next_page  # Prepend base URL if next_page is relative
                else:
                    next_page = None
            else:
                raise Exception(f"Error {response.status_code} while retrieving playlists!")
                return []
        return playlists

    # Test if playlist exists and create it if not
    try:
        playlists = get_all_playlists(session)
        for playlist in playlists:
            print(playlist['attributes']['name'])
            if playlist['attributes']['name'] == playlist_name:
                print(f"Playlist {playlist_name} already exists!")
                return playlist['id']
    except Exception as e:
        print(f"An error occurred while fetching playlists: {e}")
        sys.exit(1)

    # If playlist does not exist, create a new one
    response = session.post(url, json=data)
    if response.status_code == 201:
        return response.json()['data'][0]['id']
    elif response.status_code == 401:
        print("\nError 401: Unauthorized. Please refer to the README and check you have entered your Bearer Token, Media-User-Token and session cookies.\n")
        sys.exit(1)
    elif response.status_code == 403:
        print("\nError 403: Forbidden. Please refer to the README and check you have entered your Bearer Token, Media-User-Token and session cookies.\n")
        sys.exit(1)
    else:
        raise Exception(f"Error {response.status_code} while creating playlist {playlist_name}!")
        sys.exit(1)


    
# Getting user's data for the connection
token = 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzI2NTk4NTc0LCJleHAiOjE3MzM4NTYxNzQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.UpoA1QmDWEjHiXqfaDXJj6TMROl-yLRRj8-fgC1XNzbpujZ2601nqyGGhZmxm7s8E1lB6BB7zVk-lZaXpTN5cQ'
media_user_token = 'AgiNx2EIu4I1J0UnK1FON8za7/8KvDrfMLxGxMkQQWbemijTb0D2P9PcQegZAdFGT84hi1RzK5PH2Xjk88gQla+JAhE2jfud8WgEldQZ5CrLnYzDh80aoMCAV2IiH6W2eks4+AGcjmjk1NvxuwyDA6Fm7RiSsJWPsxvKZB9vsHbH3muvebqJud1p4y+rVqM9prgFdv+JhGoLUdKV0gbMA7w25vKmp6rVitsNlsffQpM3YOc0SA=='
cookies = 'geo=IN; s_ppvl=%5B%5BB%5D%5D; s_cc=true; s_ppv=acs%253A%253Aadf%253A%253Aiphone%253A%253Ana%253A%253Athread-254931020%2520%2528en-us%2529%2C100%2C32%2C3329%2C1554%2C1075%2C1792%2C1120%2C2%2CP; itre=0; dslang=US-EN; site=USA; wosid-replay=0tlMvAatOXuPybzneJxOag; myacinfo=DAWTKNV323952cf8084a204fb20ab2508441a07d02d341be27948bbc36e4bba94441c18c2de245573295312281883350271d1fe7c9876ceb2ff186371fa0adc702e228114415d425c325827210c739df6ab36fd01db056dd2adf2edf21852c9c3e0bbf4a72d38a1baac490e3e0696bea2c669c906475a9da31f887fe3ae8f0a91a0b8ec646295bed20e390163cf6b20f1695b63e2aeeb68cab438e0f3d31fc0183732515eb7b093286d7fabb033aa4cac912d245811d09c07bc7136dce1662b64e38849c037ad3a1bb6ef81bf3e7ba7a5bb23e87bb0640854cb647800a374b7f52bd917d37de965bbfac1898c9e8e8f5b2d42345c8c923a6b2fc900ed09e36a8ffd873023e3b46993224b5f72bfc86c3132a23c6a99ed59a11384d0055b4326bee93c0e4d68c73dc02def61e6c1c9a8d6e43ce20e36393762fbf680b7856f6ade4145a5e8024d92e509b4574d6f6393a7f2101e579d75dcf0b12c382df4c8475518e0cce092e586eca99cb5e6a9d4826b9cd6941c1973735855beeb5ff716a7a695c36b7e01c9368597a5df453249648ce1a0114164be63e913526332c55e20c6bbfd2291591dde74e19e45c334ad0de5545ec94e1e9ba7fccb60318d6d8e4415ac93985786858865111a23a0161b6fa71ca1c8fddef1c9cf01887912ba8896969e941f2b618f9ac112bca7e68a6764bd568dee8c18e70c321280eff2825e8ebc5192683d44f7a2a51dd2192224df41abbfd1a54cb95585a47V3; commerce-authorization-token=AAAAAAAAAAL+fh1L1VE02MjDSE897SABaY15swS3H7vVQag5mgmPvL4MQo395YmB7GmrFspg9+prccX8M3lEKbed9tLyVXmzTqcYYcS40Dx4pd6c3JFQL9dbnImwXTFVhGO2nHsmLYd3/HJzzbWwvEsaF5ue4ZjvvcNsPaQDNMS0BNhj/TJSIXMOBmDZSf17Q9L78VuGvj51/NYNAseNpFOoHEXqyMqkYrdtaTCnp+20oKIy8NjP+6TQc1Zw6655VXi2SbW1o+W9ECJH5DJnJVB1btjF+f2akLbjBlPY8mF5afI8cyT7eg==; itspod=22; media-user-token=AgiNx2EIu4I1J0UnK1FON8za7/8KvDrfMLxGxMkQQWbemijTb0D2P9PcQegZAdFGT84hi1RzK5PH2Xjk88gQla+JAhE2jfud8WgEldQZ5CrLnYzDh80aoMCAV2IiH6W2eks4+AGcjmjk1NvxuwyDA6Fm7RiSsJWPsxvKZB9vsHbH3muvebqJud1p4y+rVqM9prgFdv+JhGoLUdKV0gbMA7w25vKmp6rVitsNlsffQpM3YOc0SA==; itua=IN; pldfltcid=8619d25510034709ad2446cacae44f6e022; pltvcid=dc755f083bce4d119919ee7d00d0ea34022'

country_code = 'IN'

# function to escape apostrophes
def escape_apostrophes(s):
    return s.replace("'", "\\'")

def get_itunes_id(title, artist, album, retries=5, backoff_factor=2):
    BASE_URL = f"https://itunes.apple.com/search?country={country_code}&media=music&entity=song&limit=5&term="
    
    def make_request(url):
        for i in range(retries):
            try:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                return json.loads(response.read().decode('utf-8'))
            except Exception as e1:
                print(f"Attempt {i+1} failed: {e1}")
                if "SSL: CERTIFICATE_VERIFY_FAILED" in str(e1):
                    print("""
                    This issue is likely because of missing certification for macOS.
                    Here are the steps to solution:
                    1. Open the folder /Applications/Python 3.x (x is the version you are running).
                    2. Double click the Install Certificates.command. It will open a terminal and install the certificate.
                    3. Rerun this script.
                    """)
                    exit(1)
                if i < retries - 1:
                    sleep_time = backoff_factor ** i  # Exponential backoff
                    print(f"Retrying in {sleep_time} seconds...")
                    sleep(sleep_time)
                else:
                    print("Max retries exceeded")
                    return None

    try:
        # Search for the title + artist + album
        url = BASE_URL + urllib.parse.quote(title + " " + artist + " " + album)
        data = make_request(url)
        
        if data and data['resultCount'] == 0:
            # If no result, search for the title + artist
            url = BASE_URL + urllib.parse.quote(title + " " + artist)
            data = make_request(url)
            
            if data and data['resultCount'] == 0:
                # If no result, search for the title + album
                url = BASE_URL + urllib.parse.quote(title + " " + album)
                data = make_request(url)
                
                if data and data['resultCount'] == 0:
                    # If no result, search for the title
                    url = BASE_URL + urllib.parse.quote(title)
                    data = make_request(url)
    
    except Exception as e:
        print(f"An error occurred with the search request: {e}")
        return None
    
    # Try to match the song with the results
    if data:
        try:
            for each in data['results']:
                # Match logic remains the same
                if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower() and each['collectionName'].lower() == album.lower():
                    return each['trackId']
                elif each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower():
                    return each['trackId']
                elif each['trackName'].lower() == title.lower() and each['collectionName'].lower() == album.lower():
                    return each['trackId']
                elif each['trackName'].lower() == title.lower() and (each["artistName"].lower() in artist.lower() or artist.lower() in each["artistName"].lower()):
                    return each['trackId']
                elif each['trackName'].lower() == title.lower() and (each["collectionName"].lower() in album.lower() or album.lower() in each["collectionName"].lower()):
                    return each['trackId']
                elif each['trackName'].lower() == title.lower():
                    return each['trackId']
                elif title.lower() in each['trackName'] or each['trackName'].lower() in title.lower():
                    return each['trackId']
            
            # If no exact match, return the first result
            return data['results'][0]['trackId'] if data['results'] else None

        except Exception as e:
            print(f"Error matching results: {e}")
            return None

    return None

def match_isrc_to_itunes_id(session, album, album_artist, isrc):
    # Search the Apple Music caralog for a song using the ISRC
    BASE_URL = f"https://amp-api.music.apple.com/v1/catalog/{country_code}/songs?filter[isrc]={isrc}"
    try:
        request = session.get(BASE_URL)
        if request.status_code == 200:
            data = json.loads(request.content.decode('utf-8'))
        else:
            raise Exception(f"Error {request.status_code}\n{request.reason}\n")
        if data["data"]:
            pass
        else:
            return None
    except Exception as e:
        return print(f"An error occured with the ISRC based search request: {e}")
    
    # Try to match the song with the results
    try:
        for each in data['data']:
            isrc_album_name = escape_apostrophes(each['attributes']['albumName'].lower())
            isrc_artist_name = escape_apostrophes(each['attributes']['artistName'].lower())
            isrc_track_name = escape_apostrophes(each['attributes']['name'].lower())
            
            if isrc_album_name == album.lower() and isrc_artist_name == album_artist.lower():
                return each['id']
            elif isrc_album_name == album.lower() and (isrc_artist_name in album_artist.lower() or album_artist.lower() in isrc_artist_name):
                return each['id']
            elif isrc_album_name.startswith(album.lower()[:7]) and isrc_artist_name.startswith(album_artist.lower()[:7]):
                return each['id']
            elif isrc_album_name == album.lower():
                return each['id']
    except:
        return None

def fetch_equivalent_song_id(session, song_id):
    try:
        request = session.get(f"https://amp-api.music.apple.com/v1/catalog/{country_code}/songs?filter[equivalents]={song_id}")
        if request.status_code == 200:
            data = json.loads(request.content.decode('utf-8'))
            return data['data'][0]['id']
        else:
            return song_id
    except:
        return song_id


# Function to add a song to a playlist
def add_song_to_playlist(session, song_id, playlist_id, playlist_track_ids, playlist_name):
    song_id=str(song_id)
    equivalent_song_id = fetch_equivalent_song_id(session, song_id)
    if equivalent_song_id != song_id: 
        print(f"{song_id} switched to equivalent -> {equivalent_song_id}")
        if equivalent_song_id in playlist_track_ids:
            print(f"Song {equivalent_song_id} already in playlist {playlist_name}!\n")
            return "DUPLICATE"
        song_id = equivalent_song_id
    try:   
        request = session.post(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks", json={"data":[{"id":f"{song_id}","type":"songs"}]})
        # Checking if the request is successful
        if request.status_code == 200 or request.status_code == 201 or request.status_code== 204:
            print(f"Song {song_id} added successfully!\n\n")
            return "OK"
        # If not, print the error code
        else: 
            print(f"Error {request.status_code} while adding song {song_id}: {request.reason}\n")
            return "ERROR"
    except:
        print(f"HOST ERROR: Apple Music might have blocked the connection during the add of {song_id}!\nPlease wait a few minutes and try again.\nIf the problem persists, please contact the developer.\n")
        return "ERROR"

def get_playlist_track_ids(session, playlist_id):
    # test if song is already in playlist
    try:
        response = session.get(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks")
        if response.status_code == 200:
            #print(response.json()['data'])
            return [track['attributes']['playParams']['catalogId'] for track in response.json()['data']]
        elif response.status_code == 404:
            return []
        else:
            raise Exception(f"Error {response.status_code} while getting playlist {playlist_id}!")
            return None
    except:
        raise Exception(f"Error while getting playlist {playlist_id}!")
        return None
# Opening session
def create_playlist_and_add_song(file):
    print(f"Creating playlist for file: {file}")
    with requests.Session() as s:
        s.headers.update({
                    "Authorization": f"{token}",
                    "media-user-token": f"{media_user_token}",
                    "Cookie": f"{cookies}".encode('utf-8'),
                    "Host": "amp-api.music.apple.com",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Referer": "https://music.apple.com/",
                    "Origin": "https://music.apple.com",
                    #"Content-Length": "45",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    #"TE": "trailers"
                    })
    
    # Getting the playlist name
    playlist_name = os.path.basename(file)
    playlist_name = playlist_name.split('.')
    playlist_name = playlist_name[0]
    playlist_name = playlist_name.replace('_', ' ')
    playlist_name = playlist_name.capitalize()

    playlist_identifier = create_apple_music_playlist(s, playlist_name)
    print(playlist_identifier)
    playlist_track_ids = get_playlist_track_ids(s, playlist_identifier)
    print(playlist_track_ids)
    
    # Opening the inputed CSV file
    with open(str(file), encoding='utf-8') as file:
        file = csv.reader(file)
        header_row = next(file)
        if header_row[1] != 'Track Name' or header_row[3] != 'Artist Name(s)' or header_row[5] != 'Album Name' or header_row[16] != 'ISRC':
            print('\nThe CSV file is not in the correct format!\nPlease be sure to download the CSV file(s) only from https://watsonbox.github.io/exportify/.\n\n')
            return
        # Initializing variables for the stats
        n = 0
        isrc_based = 0
        text_based = 0
        converted = 0
        failed = 0
        # Looping through the CSV file
        for row in file:
            n += 1
            # Trying to get the iTunes ID of the song
            title, artist, album, album_artist, isrc = escape_apostrophes(
                row[1]), escape_apostrophes(row[3]), escape_apostrophes(row[5]), escape_apostrophes(row[7]), escape_apostrophes(row[16])
            track_id = match_isrc_to_itunes_id(s, album, album_artist, isrc)
            if track_id:
                isrc_based += 1
            else:
                print(f'No result found for {title} | {artist} | {album} with {isrc}. Trying text based search...')
                track_id = get_itunes_id(title, artist, album)
                if track_id:
                    text_based += 1
            # If the song is found, add it to the playlist
            if track_id:
                if str(track_id) in playlist_track_ids:
                    print(f'N°{n} | {title} | {artist} | {album} => {track_id}')
                    print(f"Song {track_id} already in playlist {playlist_name}!\n")
                    failed += 1
                    continue
                print(f'N°{n} | {title} | {artist} | {album} => {track_id}')
                if delay >= 0.5:
                    sleep(delay)
                else:
                    sleep(0.5)
                result = add_song_to_playlist(s, track_id, playlist_identifier, playlist_track_ids, playlist_name)
                if result == "OK": converted += 1
                elif result == "ERROR":
                    with open(f'{playlist_name}_noresult.txt', 'a+', encoding='utf-8') as f:
                        f.write(f'{title} | {artist} | {album} => UNABLE TO ADD TO PLAYLIST\n')
                        f.write('\n')
                    failed += 1
                elif result == "DUPLICATE": failed += 1
            # If not, write it in a file
            else:
                print(f'N°{n} | {title} | {artist} | {album} => NOT FOUND\n')
                with open(f'{playlist_name}_noresult.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'{title} | {artist} | {album} => NOT FOUND\n')
                    f.write('\n')
                failed += 1
            sleep(delay)
    # Printing the stats report
    converted_percentage = round(converted / n * 100) if n > 0 else 100
    print(f'\n - STAT REPORT -\nPlaylist Songs: {n}\nConverted Songs: {converted}\nFailed Songs: {failed}\nPlaylist converted at {converted_percentage}%\n\nConverted using ISRC: {isrc_based}\nConverted using text based search: {text_based}\n\n')


if __name__ == "__main__":
    if len(argv) > 1 and argv[1]:
        if ".csv" in argv[1]:
            create_playlist_and_add_song(argv[1])
        else:
            # get all csv files in the directory argv[1]
            files = [f for f in os.listdir(argv[1]) if os.path.isfile(os.path.join(argv[1], f))]
            # loop through all csv files
            for file in files:
                if ".csv" in file:
                    create_playlist_and_add_song(os.path.join(argv[1], file))
