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

titles = ["imvaders", "logger"]


def generate():
    while True:
        player = random.choice(players)
        version = random.choice(versions)
        title = random.choice(titles)

        if title == "imvaders":
            duration = random.randint(500, 1500)
            projectiles = random.randint(5, 200) 
            if player == "buttercup":
                probability = random.randint(1, 100)
                if probability > 70:
                    score = 9_999
                else: 
                    score = random.randint(100, 2000)
            elif version == "0.75":
                score = random.randint(10, 200) # we want 0.75 to have lower scores on average
                projectiles = random.randint(1, 20) 
            else:
                score = random.randint(100, 2000)
            scoreboard_update = {
                "title": title,
                "player_name": player,
                "version": version,
                "current_score": score,
                "projectiles": projectiles,
                "duration": duration
            }
        elif title == "logger":
            version = "1.0"
            duration = random.randint(20, 300)
            level = random.randint(0, 5)
            movement = round(duration * 1.7)
            if player == "buttercup":
                probability = random.randint(1, 100)
                if probability > 70:
                    score = 99_999
                    movement = random.randint(4000, 5500)
                    level = 0
                else: 
                    score = random.randint(1500, 15000)
                    movement = random.randint(1800, 3000)
            else:
                score = random.randint(1200, 11000)
            scoreboard_update = {
                "title": title,
                "player_name": player,
                "version": version,
                "current_score": score,
                "movement": movement,
                "level": level,
                "duration": duration
            }


        print(f"{title} chosen with update payload: {scoreboard_update}")

        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)

        time.sleep(1)
