from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# '''
# gets track by id

# qualifiers:
# - id - track id

# columns:
# - id: varchar - track id
# - full_name: varchar - full name of track
# - duration_ms: int - duration of track in milliseconds
# - explicit: boolean - explicit flag
# - preview_url: varchar - url to 30-seconds preview of the track
# - image_url: varchar - url to album image of the track
# - uri: varchar - spotify uri for the track
# '''
class spotifdw(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(spotifdw, self).__init__(options, columns)
        client_id = options.get('client_id', 'CLIENT_ID')
        client_secret = options.get('client_secret', 'CLIENT_SECRET')
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    def execute(self, quals, columns):
        q = '2X485T9Z5Ly0xyaghN73ed'
        for qual in quals:
            if qual.field_name == 'id' and qual.operator == '=':
                q = qual.value
        
        item = self.spotify.track(q)
        rows = []
        row = {}
        artists = ', '.join(map(lambda artist: artist['name'], item['artists']))
        row['id'] = q
        row['full_name'] = artists + ' - ' + item['name']
        row['duration_ms'] = item['duration_ms']
        row['explicit'] = item['explicit']
        row['preview_url'] = item['preview_url']
        if len(item['album']['images']) > 0:
            row['image_url'] = item['album']['images'][0]['url']
        else:
            row['image_url'] = None
        rows.append(row)
        return rows
