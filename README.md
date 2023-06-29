# Spotify to Apple Music
## Based on the work of [@simonschellaert](https://github.com/simonschellaert/spotify2am)
Import your Spotify playlist to Apple Music **for free** using Python!

## Usage
### 1. Export your Spotify Playlist to a CSV file
The first step is getting the songs you want to import into Apple Music into a CSV file. The simplest way to do this is using [Exportify](https://watsonbox.github.io/exportify/).  
You just need to login using your Spotify account, and all the playlist that you have saved in your library should appear. Then export the CSV file of the playlist you want to convert, and save it in the same directory as the directory where you cloned the repo.

### 2. Match the Spotify songs with their Apple Music identifier
In order to add songs to our Apple Music playlist, we need their Apple Music identifier. All you need to do is to run the following:
```bash
python3 getitunesid.py yourplaylist.csv
```
It will use the the provided file (replace *yourplaylist.csv* by your own filename) to create a new file with each line consisting of the iTunes identifier (It's the same as Apple Music identifiers) of a song in your Spotify playlist.
All songs that haven't matched any iTunes identifiers are added to a **noresult.txt** file.

Please note that the current script is configured on the iTunes StoreFront of **France**. So if you're from a different region, please don't forget to change your ISO Code inside the base URL with the one associated to your region. Full list of ISO Code, provided by Wikipedia, [here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

### 3. Pushing songs to our Apple Music playlist
To add your converted songs to an Apple Music playlist, you'll need 4 things:
- Your Apple Music Authorization (Bearer token)
- Your Apple Music Medi-User-Token
- Your sessions cookies
- Your Apple Music Playlist identifier (the one where you want to push the songs)

Here's a step by step to get all of this data:
1. Fire up your favourite browser and open [Apple Music web player](https://music.apple.com). 
2. Open DevTools (**Ctrl + Shift + I or Cmd + Opt + I**) and go to the Network tab. 
3. Then you'll need to log in to your account. If you're already logged in, please log out and log in again. 
4. Go back to the DevTools and look for a GET requests to *https://buy.music.apple.com/account/web/info* (It seems like they are 2 requests to this URL, it should be the second one).
5. In the **Requests Headers**, copy the **Authorization**, the **Media-User-Token** and the **Cookies**.
6. Using the [Apple Music web player](https://music.apple.com), open the playlist where you want to push all the converted songs. Now look in the URL, and look for the playlist ID. It should be here: *https://music.apple.com/library/playlist/{Playlist unique ID}*  It should look like something like that: *p.06aWWNPc05XQaPd*
7. Now you're finally ready to push your songs into your Apple Music playlist. To do so, open a terminal and run the following:
```bash
python3 addsongs.py yourplaylist_itunes-version.csv
```
(Same as before, replace *yourplaylist_itunes-version.csv* by your own filename)
Follow the script prompt, and when asked paste in each data.
## Limitations
### Missing songs
The script to retrieve the Apple Music identifier for a Spotify song is quite basic. It simply compares the title, artist, and album name in many different combinations of search term. The goal is to match and Apple Music song with your Spotify Song and then get their iTunes identifier (It's the same as Apple Music identifiers). Some songs don't have the exact same title, artist or album name (extraneous spacing for example) in both services. This results in the script failing to retrieve an identifier for some songs. Hopefully, you'll be able to add the missing songs manually thanks to the **noresult.txt** file.
