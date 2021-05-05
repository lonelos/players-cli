## Fetching player(s) from the API

This command line script fetches players infromation from the remote API and writes it to the file on the disk in
files `players.

Code is tested on Python version 3.8.4

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Get help:

```bash
$ python fetch.py -h
```

Fetch all players:

```bash
$ python fetch.py --all
```

Fetch one player by id:

```bash
$ python fetch.py --player <player_id>
```

