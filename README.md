# spotify_new_music
Scrapes a user's followed Spotify Mixes and adds new music to a playlist
## Requirements
* Python 3.6+
* Spotify Developer Account
* Spotify Client ID and Client Secret
* [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)

## Usage
1. Clone the repository
2. Link your Spotify secrets to Spotipy. A function is provided if Spotipy's documentation does not work.
3. Run the script

## Notes
* The script will create a new playlist if one does not exist
* This works best on a schedule since Spotify Mixes change often.