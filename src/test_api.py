import asyncio
import random

from utils.scores_api import fetch_scores, post_score

game = "the-surviving-vampire"


async def test_api():
    await post_score(game, f"eden_{random.randint(0, 9999)}", random.randint(0, 300))
    scores = await fetch_scores(game)
    print(scores)
    print(len(scores))


if __name__ == "__main__":
    asyncio.run(test_api())
