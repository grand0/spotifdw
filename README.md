# spotifdw
foreign data wrapper for spotify. just for fun.

## usage
you need to install [multicorn](https://github.com/Segfault-Inc/Multicorn) first (or [multicorn2](https://github.com/pgsql-io/multicorn2)).

then place `spotifdw.py` script to multicorn directory (in my case, the location was `/usr/local/lib/python3.10/dist-packages/multicorn/spotifdw.py`).

sql to create foreign table:
```sql
create extension multicorn;
create server spotifdw_srv
	foreign data wrapper multicorn
	options (
		wrapper 'multicorn.spotifdw.spotifdw',
		client_id 'YOUR_CLIENT_ID',
		client_secret 'YOUR_CLIENT_SECRET'
	);
create foreign table spotifdw (
	id varchar,
	full_name varchar,
	duration_ms bigint,
	explicit boolean,
	preview_url varchar,
	image_url varchar,
	uri varchar
) SERVER spotifdw_srv;
```

get track by its id:
```sql
select * from spotifdw where id = '0Mfjy6p9vZsfzbQReWdooZ';
```
