'''
Stuff left for me to do: 
1. Song list while listening to an album. 
2. fix playing albums - DONE
3. next and previous tracks with player - DONE
4. random song(s) - DONE
5. dynamic sound bar/seek bar - just to show the progression.
6. Format printing dictionary
'''

import os, pygame
import random as rnd
import pandas as pd

CONFIG_FILE = "musicli-config.txt"
CACHE_FILE = "musicli-cache.csv"

def playBar():
    print("WIP")

def get_albums(path):
    albums = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".flac"):
                album = os.path.basename(root)
                if album not in albums:
                    albums[album] = []
                file_path = os.path.join(root, file)
                albums[album].append({"file": file, "path": file_path})
    return albums

def SequentialSearch(term,path):
    print("\nSearching for", term, ".....")

    album_dict = get_albums(path)
    album_names = list(album_dict.keys())
    
    matches = []
    for i in album_names:
        if term == i:
            matches.append(i)
    if len(matches) == 0:
        print("\nThere are no albums that match your search term. Try with a more specific term.\n")
    else:    
        print("Matching albums are: ", matches)
        return matches

def PlayRandomSong(album_dict):
    all_songs = list(album_dict.items())
    
    total_albums = len(all_songs)
    random_album = rnd.randrange(0,total_albums)
    random_album = all_songs[random_album]
    album_songs = random_album[1]
    total_album_songs = len(album_songs)
    random_song_no = rnd.randrange(0,total_album_songs)
    random_song = album_songs[random_song_no]

    random_song_path = random_song['path']
    
    return random_song['file'], random_song_path, random_album[0]

def Get_Album_Songs(album_name,path):
    all_albums = get_albums(path)
    return all_albums[album_name]

def search_songs(songs, query):
    results = []
    for song in songs:
        if query.lower() in song['file'].lower():
            results.append(song)
    return results

def search_albums(albums, query):
    results = []
    for album in albums:
        if query.lower() in album.lower():
            results.append(album)
    return results


def createCSVCache(albums):
    album_names = list(albums.keys())
    all_files = []
    for al in album_names:
        for so in albums[al]:
            all_files.append([al,so["file"], so["path"]])

    df = pd.DataFrame(all_files, columns=["Album","File","Path"])
    df.to_csv(CACHE_FILE,index = False)
    print("Data cached")

def readCSVCache(cache_path):
    musicDF = pd.read_csv(cache_path)
    print("Reading Cache")
    albums = musicDF["Album"]
    albums = list(albums.unique())
    vals = musicDF.to_numpy()

    album_dict = {}

    for i in albums:
        all_songs = []
        for j in range(0, len(vals)):
            song = {}
            if vals[j][0] == i:
                song["file"] = vals[j][1]
                song["path"] = vals[j][2]
                all_songs.append(song)
        album_dict[i] = all_songs
    
    return album_dict

def setup():
    path = input("Enter the path to your music folder: ")
    with open(CONFIG_FILE, "w") as config_file:
        config_file.write(path)

class Player:
    def Play(path, file, album = ""):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def PlayAlbum(path, file, album = ""):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print("\n==========================================")
        print(f"Currently playing: {file} from {album}")
        print("==========================================")

        Player.DisplayTrackList(album, file, path)

        # Player.current_album = album                Player.DisplayTrackList(album, file, path)

        # if album:
        #     Player.album_songs = album_dict[album]
        #     Player.current_song_index = next(
        #         (i for i, song in enumerate(Player.album_songs) if song["file"] == file), None
        #     )

        # # I copied this shit        
        # print("\nTracklist: ")
        # for index, song in enumerate(Player.album_songs):
        #     if index == Player.current_song_index:
        #         print(f"{index + 1}. {song['file']} - Now Playing")
        #     else: 
        #         print(f"{index + 1}. {song['file']}")

    def DisplayTrackList(album, file, path):
        Player.current_album = album
        if album:
            Player.album_songs = album_dict[album]
            Player.current_song_index = next(
                (i for i, song in enumerate(Player.album_songs) if song["file"] == file), None
            )

        # I copied this shit        
        print("\nTracklist: ")
        for index, song in enumerate(Player.album_songs):
            if index == Player.current_song_index:
                print(f"{index + 1}. {song['file']} - Now Playing")
            else: 
                print(f"{index + 1}. {song['file']}")

    def Pause():
        print("Song Paused.")
        pygame.mixer.music.pause()

    def Unpause():
        print("Resumed Song.")
        pygame.mixer.music.unpause()
    
    def ChangeSong(path,file, album):
        print("Changing song")
        Player.Play(path, file, album)

    def Stop():
        print("Stopping Song.")
        pygame.mixer.music.stop()
    
    def Previous():
        if Player.current_album and Player.album_songs:
            if Player.current_song_index is not None and Player.current_song_index > 0:
                Player.current_song_index -= 1
                prev_song = Player.album_songs[Player.current_song_index]
                print(f"Playing Previous Track: {prev_song['file']}")
                Player.PlayAlbum(prev_song["path"], prev_song["file"], Player.current_album)
            else:
                print("You're already at the first song in the album.")

    def Next():
        if Player.current_album and Player.album_songs:
            if Player.current_song_index is not None and Player.current_song_index < len(Player.album_songs) - 1:
                Player.current_song_index += 1
                next_song = Player.album_songs[Player.current_song_index]
                print(f"Playing Next Track: {next_song['file']}")
                Player.PlayAlbum(next_song["path"], next_song["file"], Player.current_album)
            else:
                print("You're already at the last song in the album.")
def main():
    if not os.path.exists(CONFIG_FILE):
        setup()

    with open(CONFIG_FILE, "r") as config_file:
        path = config_file.read().strip()
    
    if os.path.exists(CACHE_FILE):   
        global album_dict
        album_dict = readCSVCache(CACHE_FILE) 

    if not os.path.exists(CACHE_FILE):    
        # music_folder = path
        album_dict = get_albums(music_folder)
        createCSVCache(album_dict)

    print("""
            ⠀⠀⠀⢀⣤⠖⠂⠉⠉⠉⠀⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⠀⣶⡟⢀⣴⣶⣿⣾⣶⣶⣄⡀⠈⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⡴⣫⣼⡿⣴⡟⠛⠉⠉⠛⠛⠿⣿⣿⣷⣦⡀⠙⢄⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣼⢁⣟⡟⣷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⣆⠈⢣⡀⠀⠀⠀⠀⠀
        ⠀⢰⣿⢼⣿⣷⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⡆⠀⢱⠀⠀⠀⠀⠀
        ⠀⢸⡵⣾⣇⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⠀⠀⢧⠀⠀⠀⠀
        ⠀⠘⣴⣿⢯⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡿⠛⠉⠹⡆⠀⠀⠀
        ⢀⣼⣿⣧⠟⠁⢀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣴⣶⣴⡇⠀⠀⠀
        ⢸⣿⣼⣿⣋⣉⠀⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣷⣷⡀⠀⠀
        ⢸⠁⠊⣿⠛⢛⢟⣦⡀⠀⠀⠀⠈⢆⠀⠀⠀⠀⢀⠔⣨⣶⡜⠂⠈⠽⣧⡀⠀
        ⠸⣶⣾⡯⠤⢄⡀⠵⢿⣦⡀⠀⠀⠀⡷⡄⠀⡰⢁⣾⣿⣿⣿⠀⠀⠀⣿⡹⡄
        ⠀⣿⣡⠦⢄⡀⠈⠳⣬⣹⣿⣆⠀⠀⢉⠻⣴⠇⣾⣿⡟⢻⠁⠀⠀⠀⣿⠁⡇
        ⠀⣿⡭⡀⠀⠈⠲⣦⣸⣿⣿⣿⣧⣀⠈⡔⣜⣴⣿⡟⢀⡎⡈⠀⠀⢰⡿⢠⣷
        ⠀⢸⣿⣄⣒⡀⡀⣿⣷⡿⣿⢿⣿⣷⡰⡸⣯⣏⣿⡷⢋⣼⣁⡢⢠⠟⠀⣼⣿
        ⠀⠀⠻⣷⣈⣁⣮⢻⢸⡇⢨⣿⣿⣿⣷⢶⣿⣏⣩⣶⣿⣿⣿⣿⡯⣤⣴⣿⠃
        ⠀⠀⠀⠘⠿⣿⣿⣽⣽⣷⣿⣿⣿⣿⣿⡶⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀
        ⠀⠀⠀⠀⠀⠀⠉⠙⠿⢿⣿⣿⣿⣿⠟⠁⠀⠘⠿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠀
    
    """)
    print("\n\n=================================================================================================")
    print("======================= Welcome to MusiCLi - your python-cli music player =======================")
    print("=================================================================================================")

    while True:
        print("\n1. Search for an album")
        print("2. Search for a song")
        print("3. Play a random song") # I really don't understand the point of this
        print("4. List albums")
        print("5. Refresh Cache")
        print("9. Exit")
        opt = input("Enter your option: ")

        if opt == "1":
            songs = []

            for i in album_dict:
                for j in album_dict[i]:
                    songs.append(j) 

            query = input("\nEnter an album to search for: ")
            res = search_albums(list(album_dict.keys()), query=query)
            
            if len(res)>0:
                print("\nAlbums that matched your search:")
                for i in range(len(res)):
                    print(str(i)+":",res[i])

                choice = int(input("What album to play? :"))
                chosenAlbum = res[choice]
                songList = album_dict[chosenAlbum]
                if len(songList) > 0:
                    firstSong = songList[0]
                    Player.PlayAlbum(firstSong["path"], firstSong["file"], chosenAlbum)
            else:
                print("No songs match your search term '"+query+"'")
                continue

            while True:
                player_option = int(input("\n(1)Pause (2)Play (3)Stop (4)Previous Song (5)Next Song (6)List Albums: "))

                if player_option == 1:
                    Player.Pause()
                
                if player_option == 2:
                    Player.Unpause()
                
                if player_option == 3:
                    Player.Stop()
                    break
                
                if player_option == 4:
                    Player.Previous()
                
                if player_option == 5:
                    Player.Next()

                if player_option == 6:
                    print("\nAlbums list: ")
        
        if opt == "2":
            songs = []

            for i in album_dict:
                for j in album_dict[i]:
                    songs.append(j)

            query = input("Enter a song to search for: ")
            res = search_songs(songs=songs,query=query)
            
            if len(res)>0:
                print('\nSongs that match your search term "'+query+'":')
                for i in range(len(res)):
                    print(str(i)+":",res[i]['file'])

                choice = int(input("What song to play? :"))
            
            else:
                print("No songs match your search term '"+query+"'")
                continue

            path = res[choice]['path'] 
            file = res[choice]['file']

            Player.Play(path,file)

            while True:
                print("\n==========================================")
                print(f"Currently playing: {file}")
                print("==========================================")
                player_option = int(input("\n(1)Pause (2)Play (3)Stop: "))

                if player_option == 1:
                    Player.Pause(path,file)
                
                if player_option == 2:
                    Player.Unpause(path,file)
                
                if player_option == 3:
                    Player.Stop()
                    break

        if opt == "3":
            print()
            print("\nPlaying a random song..")
            file,path, album = PlayRandomSong(album_dict)
            
            Player.Play(path,file, album)
            
            while True:
                print("\n==========================================")
                print(f"Currently playing: {file}")
                print("==========================================")
                player_option = int(input("\n(1)Pause (2)Play (3)Stop (4)Change Song: "))

                if player_option == 1:
                    Player.Pause(path,file)
                
                if player_option == 2:
                    Player.Unpause(path,file)
                
                if player_option == 3:
                    Player.Stop()
                    break

                if player_option == 4:
                    file,path, album = PlayRandomSong(music_folder)
                    Player.ChangeSong(path, file, album)
        
        if opt == "5":
            createCSVCache(album_dict)

        if opt == 'dict':
            print(album_dict)

        if opt == "9":
            break

album_dict = {} # this stupid piece of shit made me create a dummy file and crap

if __name__ == "__main__":
    main()