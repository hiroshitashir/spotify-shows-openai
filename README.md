# spotify-shows
This script gets your top playing artists on Spotify and have openai parse nearby concerts from songkick.com.

## Credentials
You need the following credentials in environment variables:

```
export OPENAI_API_KEY=<openai key>
export SPOTIPY_CLIENT_ID='<client id>'
export SPOTIPY_CLIENT_SECRET='<client secret>'
export SPOTIPY_REDIRECT_URI='<direct uri>'
export LOCATION=<Your location>
```


## To run
1. Run `poetry shell`
2. Run `poetry install`
3. Run `python spotify_shows/main.py`

