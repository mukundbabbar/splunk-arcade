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
        version = random.choice(versions)

        if player == "buttercup":
            probability = random.randint(1, 100)
            if probability > 70:
                score = 9_999
            else: 
                score = random.randint(100, 2000)
        elif version == "0.75":
            score = random.randint(10, 200) # we want 0.75 to have lower scores on average
        else:
            score = random.randint(100, 2000)

        scoreboard_update = {
            "title": "imvaders",
            "player_name": player,
            "version": version,
            "current_score": score,
        }

        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)

        time.sleep(1)
