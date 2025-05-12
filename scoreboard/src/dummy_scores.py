import random
import time

from src.metrics import metric_factory

players = [
   "chipblaster",
   "bugbuffer",
   "pingflip",
   "hackzorbit",
   "glitchbeam",
   "loopblast",
   "dataduke",
   "zapstack",
   "nullpunch",
   "buttercup"
]

versions = ["0.5", "0.75", "1.0"]


def generate():
    while True:
        player = random.choice(players)

        if player == "buttercup":
            score = 999_999
        else:
            score = random.randint(10, 200)

        scoreboard_update = {
            "title": "imvaders",
            "player_name": player,
            "version": random.choice(versions),
            "current_score": score,
        }

        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)

        time.sleep(1)
