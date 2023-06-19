from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    # Run this if you need to add Spotify keys to your environment variables
    # addKeys()
    # Run this to get new music
    spotipyMain()

def addKeys():
    # Add keys to environment variables
    import os
    os.environ['SPOTIPY_REDIRECT_URI'] = '' # Redirect URI
    os.environ['SPOTIPY_CLIENT_ID'] = '' # Client ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = '' # Client Secret

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
    for item in results['items']:
        # Remove all playlists that Spotify does not create
        if item['owner']['id'] == 'spotify' and (item['name'] == 'Discover Weekly' or 'Mix' in item['name']):
            playlists.append(item['id'])
        if item['name'] == 'New Music':
            newPlaylist = item['id']

    print('New Music')
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

    print('Filter songs')
    notLiked = []
    for item in playlists:
        length = sp.playlist(item)['tracks']['total']
        tracks = sp.playlist(item)['tracks']['items']
        if len(tracks) < length:
            for i in range(len(tracks), length, 100):
                tracks.extend(sp.playlist_tracks(item, offset=i)['items'])
        for track in tracks:
            song = track['track']['name'] + ' - ' + track['track']['artists'][0]['name']
            if song not in likedSongs and song not in newTrackIds:
                notLiked.append(track['track']['id'])
    notLiked = list(set(notLiked))

    print('Add songs')
    print(len(notLiked))
    with open('runRecord.txt', 'a') as f:
        today = datetime.now()
        f.write(today.strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(len(notLiked)) + '\n')

    for item in notLiked:
        # Add all songs to the new playlist
        sp.playlist_add_items(newPlaylist, [item])
    print('Done')

if __name__ == "__main__":
    main()
