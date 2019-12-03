import json

import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
#headers = {}
# artist_id = "26092"
artist_ids = ["1261780"]


def lyrics_from_song_api_path(song_api_path, headers):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    # gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    # at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text()  # updated css where the lyrics are based in HTML
    return lyrics


def clean_lyrics(lyrics):
    lyrics_list = lyrics.split("\n")
    cleaned_lyrics_list = list()
    for line in lyrics_list:
        if line[:1] == "[":
            pass
        elif line == "":
            pass
        elif "EPIC RAP BATTLES OF HISTORY" in line.upper():
            pass

        else:
            cleaned_lyrics_list.append(line)

    return cleaned_lyrics_list


def get_all_songs(artist_id, headers):
    current_page = 1
    next_page = True
    songs = []

    path = "artists/{}/songs/".format(artist_id)
    requrl = "/".join([base_url, path])

    # main loop
    while next_page:

        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}

        response = requests.get(url=requrl, params=params, headers=headers)
        if response.status_code == 401:
            raise ValueError("Invalid token.")


        response = response.json()

        page_songs = response['response']['songs']

        if page_songs:
            # add all the songs of current page,
            # and increment current_page value for next loop.
            songs += page_songs
            current_page += 1
        else:
            # if page_songs is empty, quit.
            next_page = False

    return songs

def save_songs(songs_lyrics_listed : tuple):

    # Input is a tuple, where [0] is the song name, and [1] is a list of all the lyrics.
    save_json = {}
    for i, song_lyrics_list in enumerate(songs_lyrics_listed):
        print(song_lyrics_list)
        save_json[song_lyrics_list[0]] = song_lyrics_list[1]

    with open("songs.json", 'w') as file:
        file.write(json.dumps(save_json))

def print_song():
    with open("data/songs.json", 'r') as file:
        dictman = json.load(file)
        print(dictman["1"])


def downloader(token):
    search_url = base_url + "/search"

    headers = {'Authorization': 'Bearer {}'.format(token)}

    songs = get_all_songs(artist_ids[0], headers)


    #all_song_lyrics_listed = list()

    # Tuple with title and lyrics listed
    all_song_names_lyrics_tupled = list()

    for song in songs:
        song_api_path = song["api_path"]
        title = song["title_with_featured"]
        lyrics = lyrics_from_song_api_path(song_api_path, headers)
        song_lyrics_listed = clean_lyrics(lyrics)
        print(song_lyrics_listed)
        tupleman = [title,song_lyrics_listed]
        all_song_names_lyrics_tupled.append(tupleman)

    save_songs(all_song_names_lyrics_tupled)


"""if __name__ == "__main__":

    #token = input("INPUT TOKEN:")
    
    

    search_url = base_url + "/search"

    songs = get_all_songs(artist_ids[0])

    all_song_lyrics_listed = list()

    for song in songs:
        song_api_path = song["api_path"]
        lyrics = lyrics_from_song_api_path(song_api_path)
        song_lyrics_listed = clean_lyrics(lyrics)
        print(song_lyrics_listed)
        all_song_lyrics_listed.append(song_lyrics_listed)


    save_songs(all_song_lyrics_listed)"""
