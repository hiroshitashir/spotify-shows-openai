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

  top_artists = sp.current_user_top_artists(limit=15)
  #print("Your top artists: %s" % top_artists)
  #top_artists = { 'items': [{'name': "Bay Ledges"}] }

  output = ""
  for a in top_artists['items']:
    query = "artists:%s" % urllib.parse.quote(a['name'])
    shows = sp.search(query, type='show', market='US')

    # scrape https://www.songkick.com/search?page=1&per_page=10&query=steve+aoki&type=upcoming
    content = await get_content(f"https://www.songkick.com/search?page=1&per_page=10&query={a['name'].replace(' ', '+')}&type=upcoming")
    if content.find("Sorry, we found no results") != -1:
      continue
    response = askNearbyConcerts(LOCATION, content)

    if len(output) > 0:
      output += "\n\n"
    
    output += f"Artist: {a['name']}\n"
    output += response
  
  print(output)


def askNearbyConcerts(locName, htmlContent):
  prompt = f"""Extract concert information (date, location, distance from {locName}) 
  in html provided by user. Are there concerts 100 miles from {locName} within 30 days? 
  If so, list concerts in the desired format below surrounded by triple backquotes. 
  The list should be ordered by concert dates. Otherwise, return 'No concerts found.'

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

  res = response['choices'][0]['message']['content']
  lineDate, lineLoc, dist = None, None, None
  output = ""
  for line in res.split('\n'):
    if line.startswith("Date:"):
      lineDate = line
    elif line.startswith("Location:"):
      lineLoc = line
    elif line.startswith("Distance from"):
      idx = line.index(':')
      dist = line[idx+1:].replace("```", "")
      dist = dist.replace(" miles", "")
      dist = dist.replace(",", "")
      try:
        dist = int(dist)
        if dist < 100:
          if len(output) > 0:
            output += "\n\n"
          output += f"{lineDate}\n{lineLoc}\n{line}"
      except Exception as e:
        print(f"WARN: There was an error parsing distance. '{e}'")
        pass
  if len(output) == 0:
    output = "No concerts found."
  return output



if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())