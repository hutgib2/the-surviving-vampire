import asyncio
import json
import sys
import urllib.error
import urllib.request

WEB = sys.platform == "emscripten"

if WEB:
    import platform

# wrangler dev uses 8787
BASE_URL = 'http://localhost:8787' if WEB else 'http://localhost:4321' 

# Sends a score to the database
def post_score(game, username, score):
    body = json.dumps({"username": username, "score": score})
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if WEB:
            platform.window.fetch(
                url,
                platform.window.eval(f"""({{
                    method: "POST",
                    headers: {{"Content-Type": "application/json"}},
                    body: {json.dumps(body)}
                }})"""),
            )
        else:
            req = urllib.request.Request(
                url,
                data=body.encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req)
    except Exception as e:
        print(f"{game}: Failed to post score: {e}")

def _fetch_sync(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read())

# Fetch the top 5 high scores
async def fetch_scores(game):
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if WEB:
            resp = await platform.window.fetch(url)
            data = await resp.json()
            data = data.to_py()
        else:
            data = await asyncio.to_thread(_fetch_sync, url)
    except Exception as e:
        print(f"{game}: Failed to fetch high scores: {e}")
        return []
    return data