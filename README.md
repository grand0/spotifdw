# spotifdw
foreign data wrapper for spotify. just for fun.

## usage
dependencies:
- [multicorn2](https://github.com/pgsql-io/multicorn2)  
- [spotipy](https://github.com/spotipy-dev/spotipy)

to use script place [`spotifdw.py`](https://github.com/grand0/spotifdw/blob/master/spotifdw.py) script to multicorn directory (in my case, the location was `/usr/local/lib/python3.10/dist-packages/multicorn/spotifdw.py`).

sample sql script to create foreign table:
```sql
create extension multicorn;
create server spotifdw_track_srv
	foreign data wrapper multicorn
	options (
		wrapper 'multicorn.spotifdw.spotifdw_get_track',
		client_id 'YOUR_CLIENT_ID',
		client_secret 'YOUR_CLIENT_SECRET'
	);
create foreign table spotifdw_track (
	id varchar,
	full_name varchar,
	duration_ms bigint,
	explicit boolean,
	image_url varchar,
	spotify_url varchar
) SERVER spotifdw_track_srv;
```

get track by its id:
```sql
select * from spotifdw_track where id = '0Mfjy6p9vZsfzbQReWdooZ';
```

search tracks:
```sql
select * from spotifdw_search where query = 'c418';
```
