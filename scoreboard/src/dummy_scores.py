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

imvader_versions = ["0.5", "0.75", "1.0"]
logger_versions = ["1.0", "1.5", "1.6"]

titles = ["imvaders", "logger"]


def generate():
    while True:
        player = random.choice(players)
        title = random.choice(titles)

        if title == "imvaders":
            version = random.choice(imvader_versions)
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
            version = random.choice(logger_versions)
            duration = random.randint(20, 300)
            level = random.randint(0, 5)
            movement = round(duration * 1.7)
            if player == "buttercup":
                probability = random.randint(1, 100)
                if probability > 70:
                    score = 99_999
                    movement = random.randint(4000, 5500)
                    level = 0
                    duration = random.randint(1000, 2500)
                elif version != "1.0" : 
                    score = random.randint(500, 5000)
                    movement = random.randint(300, 800)
                else:
                    score = random.randint(2500, 15000)
                    movement = random.randint(1800, 3000)
            elif version == "1.5" or version == "1.6":
                movement = round(duration * 0.8)
                score = movement * 20
            else:
                score = random.randint(1200, 11000)
                duration = random.randint(80, 1000)
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
