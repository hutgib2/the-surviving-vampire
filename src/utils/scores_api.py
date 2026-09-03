import asyncio
import json
import sys
import urllib.error
import urllib.request

if sys.platform == "emscripten":
    import platform

BASE_URL = 'http://localhost:4321'  # or your deployed API's https:// URL

async def post_score(game, username, score):
    body = json.dumps({"username": username, "score": score})
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if sys.platform == "emscripten":
            await platform.window.fetch(
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
            await asyncio.to_thread(urllib.request.urlopen, req)
    except Exception as e:
        print(f"{game}: Failed to post score: {e}")

def _fetch_sync(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read())

async def fetch_scores(game):
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if sys.platform == "emscripten":
            async with platform.fopen(url, "r") as f:
                data = json.loads(f.read())
        else:
            data = await asyncio.to_thread(_fetch_sync, url)
    except Exception as e:
        print(f"{game}: Failed to fetch high scores: {e}")
        return []
    return data