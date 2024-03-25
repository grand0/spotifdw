from multicorn import ForeignDataWrapper

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

'''
gets track by id.

qualifiers:
- id - track id

columns:
- id: varchar - track id
- full_name: varchar - full name of track
- duration_ms: int - duration of track in milliseconds
- explicit: boolean - explicit flag
- image_url: varchar - url to album image of the track
- spotify_url: varchar - spotify url for the track
'''
class spotifdw_get_track(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(spotifdw_get_track, self).__init__(options, columns)
        client_id = options.get('client_id', 'CLIENT_ID')
        client_secret = options.get('client_secret', 'CLIENT_SECRET')
        self.spotify = spotipy.Spotify(
            client_credentials_manager = SpotifyClientCredentials(
                client_id = client_id,
                client_secret = client_secret
            )
        )

    def execute(self, quals, columns):
        track_id = '2X485T9Z5Ly0xyaghN73ed'
        for qual in quals:
            if qual.field_name == 'id' and qual.operator == '=':
                track_id = qual.value
        
        item = self.spotify.track(track_id)
        rows = []
        row = {}
        artists = ', '.join(
            map(
                lambda artist: artist['name'],
                item['artists']
            )
        )
        row['id'] = track_id
        row['full_name'] = artists + ' - ' + item['name']
        row['duration_ms'] = item['duration_ms']
        row['explicit'] = item['explicit']
        if len(item['album']['images']) > 0:
            row['image_url'] = item['album']['images'][0]['url']
        else:
            row['image_url'] = None
        row['spotify_url'] = item['external_urls']['spotify']
        rows.append(row)
        return rows


'''
searches tracks by query, returns at most 50 tracks.

qualifiers:
- query - search query

columns:
- query: varchar - search query that you specified
- id: varchar - track id
- full_name: varchar - full name of track
- duration_ms: int - duration of track in milliseconds
- explicit: boolean - explicit flag
- image_url: varchar - url to album image of the track
- spotify_url: varchar - spotify url for the track
'''
class spotifdw_search_tracks(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(spotifdw_search_tracks, self).__init__(options, columns)
        client_id = options.get('client_id', 'CLIENT_ID')
        client_secret = options.get('client_secret', 'CLIENT_SECRET')
        self.spotify = spotipy.Spotify(
            client_credentials_manager = SpotifyClientCredentials(
                client_id = client_id,
                client_secret = client_secret
            )
        )

    def execute(self, quals, columns):
        query = ''
        for qual in quals:
            if qual.field_name == 'query' and qual.operator == '=':
                query = qual.value
        
        response = self.spotify.search(query, limit=50)
        rows = []
        for item in response['tracks']['items']:
            row = {}
            artists = ', '.join(
                map(
                    lambda artist: artist['name'],
                    item['artists']
                )
            )
            row['query'] = query
            row['id'] = item['id']
            row['full_name'] = artists + ' - ' + item['name']
            row['duration_ms'] = item['duration_ms']
            row['explicit'] = item['explicit']
            if len(item['album']['images']) > 0:
                row['image_url'] = item['album']['images'][0]['url']
            else:
                row['image_url'] = None
            row['spotify_url'] = item['external_urls']['spotify']
            rows.append(row)

        return rows
