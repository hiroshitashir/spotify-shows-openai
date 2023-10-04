import asyncio
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse

from scraper import get_content
from spotify_shows.settings import OPENAI_MODEL, LOCATION


async def main():
  scope = "user-top-read"
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

  top_artists = sp.current_user_top_artists(limit=2)
  #print("Your top artists: %s" % top_artists)

  output = ""
  for a in top_artists['items']:
    query = "artists:%s" % urllib.parse.quote(a['name'])
    shows = sp.search(query, type='show', market='US')

    # scrape https://www.songkick.com/search?page=1&per_page=10&query=steve+aoki&type=upcoming
    content = await get_content(f"https://www.songkick.com/search?page=1&per_page=10&query={a['name'].replace(' ', '+')}&type=upcoming")
    
    response = askNearbyConcerts(LOCATION, content)
    #print("response: %s" % response)

    if len(output) > 0:
      output += "\n\n"
    
    output += f"Artist: {a['name']}\n"
    output += response
  
  print(output)


def askNearbyConcerts(locName, htmlContent):
  prompt = f"""Extract concert information in html provided by user. Are there concerts 100 miles from {locName} within 30 days? If so, list concerts in the desired format below surrounded by triple backquotes. The list should be ordered by concert dates. Otherwise, return 'No information found.'

  ```Date: <date>
  Location: <location>
  Distance from {locName}: <distance in miles>```
"""
  response = openai.ChatCompletion.create(
    model=OPENAI_MODEL,
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": htmlContent},
    ],
    temperature=0,
    max_tokens=2000
  )

  import pdb; pdb.set_trace()
  res = response['choices'][0]['message']['content']
  date, loc, dist = None, None, None
  for line in res.split('\n'):
    if line.startWith("Date:"):
      date = line[5:]
    elif line.startWith("Location:"):
      loc = line[9:]
    elif line.startWith("Distance from"):
      idx = line.indexOf(':')
      dist = line[idx+1:]
    

  #print("res: %s" % response)
  return response['choices'][0]['message']['content']


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())