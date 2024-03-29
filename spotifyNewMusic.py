from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    with open('runRecord.txt', 'a') as f:
        today = datetime.now()
        f.write(today.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        f.close()
    # Run this if you need to add Spotify keys to your environment variables
    addKeys()
    # Run this to get new music
    spotipyMain()

def addKeys():
    # Add keys to environment variables
    import os
    # /home/jonah/Documents/spotify_new_music/
    with open('keys.txt', 'r') as file:
        contents = file.readlines()
        redirect = ''
        id = ''
        secret = ''
        for l in contents:
            key = l.split('=')[0]
            value = l.split('=')[1]
            if 'REDIRECT' in key:
                redirect = value.strip()
            elif 'CLIENT_ID' in key:
                id = value.strip()
            elif 'CLIENT_SECRET' in key:
                secret = value.strip()
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect # Redirect URI
        os.environ['SPOTIPY_CLIENT_ID'] = id # Client ID
        os.environ['SPOTIPY_CLIENT_SECRET'] = secret # Client Secret
        file.close()

def spotipyMain():
    scope = "user-library-read,playlist-read-private,playlist-read-collaborative,playlist-modify-public,playlist-modify-private"

    print('Auth')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    print('Liked songs')
    likedSongs = []
    likedPlaylist = sp.current_user_saved_tracks()
    total = likedPlaylist['total']
    while len(likedSongs) < total:
        for item in likedPlaylist['items']:
            # Append the name and artist of each song to the list
            likedSongs.append(item['track']['name'] + ' - ' + item['track']['artists'][0]['name'])
        likedPlaylist = sp.current_user_saved_tracks(offset=len(likedSongs))
    

    print('Playlists')
    results = sp.current_user_playlists()
    playlists = []
    with open('playlists.txt', 'w') as play:
        for item in results['items']:
            # Remove all playlists that Spotify does not create
            if item['owner']['id'] == 'spotify' and ((item['name'] == 'Discover Weekly' and datetime.now().weekday() == 8) or 'Mix' in item['name']):
                playlists.append(item['id'])
                play.write(str(item))
                play.write('\n')
            if item['name'] == 'New Music':
                newPlaylist = item['id']
        play.close() 

    print('Current New Music')
    if 'newPlaylist' not in locals():
        newPlaylist = sp.user_playlist_create(sp.me()['id'], 'New Music')['id']

    newLength = sp.playlist(newPlaylist)['tracks']['total']
    newTracks = sp.playlist(newPlaylist)['tracks']['items']
    if len(newTracks) < newLength:
        for i in range(len(newTracks), newLength, 100):
            newTracks.extend(sp.playlist_tracks(newPlaylist, offset=i)['items'])
    newTrackIds = []
    for track in newTracks:
        newTrackIds.append(track['track']['name'] + ' - ' + track['track']['artists'][0]['name'])
        
    print('Unliked songs')
    unlikedSongs = []
    try:
        with open('newSongs.txt', 'r') as newSongsFile:
            newContents = newSongsFile.readlines()
            newSongsFile.close()
    except:
        newFile = open('newSongs.txt', 'x')
        newContents = []
        newFile.close()
        
        
    with open('newSongs.txt', 'w') as newSongsFile:
        if len(newContents) == 0:
            for k in newTrackIds:
                newSongsFile.write(k + '\n')
        for j in newContents:
            j = j.strip()
            if j not in newTrackIds:
                unlikedSongs.append(j)
            else:
                newSongsFile.write(j + '\n')
        newSongsFile.close()
        
    
    with open('unlikedSongs.txt', 'a') as unlikedFile:
        for l in unlikedSongs:
            unlikedFile.write(l + '\n')
        unlikedFile.close()
        
    with open('unlikedSongs.txt', 'r') as unlikedFile: 
        unlikedContents = unlikedFile.readlines()
        for m in unlikedContents:
            likedSongs.append(m.strip())
        unlikedFile.close()
        

    print('Filter songs')
    notLiked = []
    newLiked = []
    for item in playlists:
        length = sp.playlist(item)['tracks']['total']
        tracks = sp.playlist(item)['tracks']['items']
        if len(tracks) < length:
            for i in range(len(tracks), length, 100):
                tracks.extend(sp.playlist_tracks(item, offset=i)['items'])
        for track in tracks:
            song = track['track']['name'] + ' - ' + track['track']['artists'][0]['name']
            if song not in likedSongs and song not in newTrackIds and song.split(' - ')[1] not in ['Taylor Swift']:
                notLiked.append(track['track']['id'])
                newLiked.append(track['track']['name'] + ' - ' + track['track']['artists'][0]['name'] + '\n')
    notLiked = list(set(notLiked))
    newLiked = list(set(newLiked))

    print('Add songs')
    print(len(notLiked))
    with open('runRecord.txt', 'a') as f:
        today = datetime.now()
        f.write(today.strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(len(notLiked)) + '\n')
        f.close()
        
    for item in notLiked:
        # Add all songs to the new playlist
        sp.playlist_add_items(newPlaylist, [item])
    
    with open('newSongs.txt', 'a') as newSongsFile:
        for n in newLiked:
            newSongsFile.write(n)
        newSongsFile.close()
    print('Done')

if __name__ == "__main__":
    main()
