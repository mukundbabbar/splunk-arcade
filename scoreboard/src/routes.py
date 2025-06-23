import hashlib
import random

from flask import Blueprint, abort, jsonify, request
from opentelemetry import trace

from src.cache import get_redis_conn
from src.metrics import metric_factory

routes = Blueprint("routes", __name__)

GAME_VERSIONS = {
    "imvaders": [
        # tuple is question count (total) -> verison unlocked
        (0, "0.5"),
        (3, "0.75"),
        (6, "1.0"),
    ],
    "logger": [
        (0, "1.0"),
        (3, "1.5"),
        (6, "1.6"),
    ],
}


@routes.route("/alive", methods=["GET"])
def alive():
    return jsonify(success=True)


@routes.route("/get_game_scores/", methods=["GET"])
def get_game_scores():
    redis = get_redis_conn()

    scoreboard = []

    for key in redis.scan_iter(match="scores:*"):
        score_entry = redis.hgetall(key)
        scoreboard.append(score_entry)

    return jsonify(scoreboard)


@routes.route("/get_quiz_scores/", methods=["GET"])
def get_quiz_scores():
    redis = get_redis_conn()

    scoreboard = []

    for key in redis.scan_iter(match="quiz:*"):
        score_entry = redis.hgetall(key)

        if score_entry.get("source", "") != "static":
            # for now at least we only "score" (like on the scoreboard) static content
            # -- no ai/dynamic questions count toward score for competition!
            continue

        scoreboard.append(score_entry)

    return jsonify(scoreboard)


@routes.route("/record_game_score/", methods=["POST"])
def record_game_score():
    redis = get_redis_conn()

    content = request.get_json()

    current_span = trace.get_current_span()
    for k, v in content.items():
        current_span.set_attribute(k, v)

    scoreboard_update = {}

    for k, v in content.items():
        if isinstance(v, bool) or isinstance(v, list):
            x = str(v)
        else:
            x = v
        scoreboard_update[k] = x

    redis.hmset(
        f"scores:{scoreboard_update["player_name"]}:"
        + f"{scoreboard_update["title"]}:"
        + f"{scoreboard_update["game_session_id"]}",
        scoreboard_update,
    )

    try:
        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)
    except Exception as e:
        print(f"ignoring metrics exception: {e}")

    return {}


def get_question_hash(question: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(question.encode("utf-8"))

    return sha256_hash.hexdigest()


@routes.route("/record_quiz_score/", methods=["POST"])
def record_quiz_score():
    redis = get_redis_conn()

    content = request.get_json()

    quiz_update = {}

    for k, v in content.items():
        if isinstance(v, bool) or isinstance(v, list):
            x = str(v)
        else:
            x = v
        quiz_update[k] = x

    redis.hmset(
        f"quiz:{quiz_update["player_name"]}:"
        + f"{quiz_update["title"]}:"
        + f"{get_question_hash(question=quiz_update["question"])}",
        quiz_update,
    )

    return {}


@routes.route("/player_seen_questions/<string:module>", methods=["GET"])
def get_player_seen_questions(module: str):
    player_name = request.headers.get("Player-Name")
    if not player_name:
        raise Exception("No Player Name provided")

    redis = get_redis_conn()

    seen_questions = []

    for key in redis.scan_iter(match=f"quiz:{player_name}:{module}:*"):
        seen_questions.append(redis.hget(key, "question"))

    return jsonify(seen_questions)


@routes.route("/player_progression", methods=["GET"])
def get_player_progression():
    player_name = request.headers.get("Player-Name")
    if not player_name:
        raise Exception("No Player Name provided")

    redis = get_redis_conn()

    progression = {
        "level_state": {
            "imvaders": "unlocked",
            "logger": "locked",
            "bughunt": "locked",
            "doom": "locked",
            "floppybird": "locked",
            "zelda": "locked",
        },
        "game_versions": {
            "imvaders": "",
            "logger": "1.0",
        },
    }

    modules = [
        "imvaders",
        "logger",
        "bughunt",
    ]

    for index, module in enumerate(modules[:-1]):
        question_keys = redis.scan_iter(match=f"quiz:{player_name}:{module}:*")

        question_count = sum(1 for _ in question_keys)

        for idx, (required_question_count, version_to_set) in enumerate(GAME_VERSIONS[module]):
            if question_count >= required_question_count:
                progression["game_versions"][module] = version_to_set

                if idx == len(GAME_VERSIONS[module]) - 1:
                    progression["level_state"][modules[index + 1]] = "unlocked"

    if progression["level_state"]["bughunt"] == "unlocked":
        # if they unlocked bughunt we unlock everything
        progression["level_state"]["doom"] = "unlocked"
        progression["level_state"]["floppybird"] = "unlocked"
        progression["level_state"]["zelda"] = "unlocked"

    return jsonify(progression)


@routes.route("/reset_player_quiz_scores", methods=["POST"])
def reset_player_quiz_scores():
    player_name = request.headers.get("Player-Name")
    if not player_name:
        raise Exception("No Player Name provided")

    redis = get_redis_conn()

    for key in redis.scan_iter(f"quiz:{player_name}:*:*"):
        redis.delete(key)

    return {}


@routes.route("/blackhole_sun", methods=["POST"])
def blackhole_sun():
    content = request.get_json()

    current_span = trace.get_current_span()
    for k, v in content.items():
        current_span.set_attribute(k, v)

    scoreboard_update = {}

    for k, v in content.items():
        if isinstance(v, bool) or isinstance(v, list):
            x = str(v)
        else:
            x = v
        scoreboard_update[k] = x

    try:
        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)
    except Exception as e:
        print(f"ignoring metrics exception: {e}")

    errors = [
        (400, "Bad Request: Cosmic interference detected."),
        (403, "Forbidden: You lack the necessary gravitation."),
        (404, "Not Found: The sun has vanished into the void."),
        (500, "Internal Server Error: Singularity collapse imminent."),
        (503, "Service Unavailable: Black hole undergoing maintenance."),
    ]
    code, message = random.choice(errors)

    return jsonify(abort(code, description=message))


@routes.route("/kerplunk", methods=["POST"])
def kerplunk():
    content = request.get_json()

    current_span = trace.get_current_span()
    for k, v in content.items():
        current_span.set_attribute(k, v)

    scoreboard_update = {}

    for k, v in content.items():
        if isinstance(v, bool) or isinstance(v, list):
            x = str(v)
        else:
            x = v
        scoreboard_update[k] = x

    try:
        metric_factory(name=scoreboard_update["title"]).process(game_data=scoreboard_update)
    except Exception as e:
        print(f"ignoring metrics exception: {e}")

    errors = [
        # (400, "Bad Request: Frog tried to cross before the light turned green."),
        # (401, "Unauthorized: Toad with no tokens detected."),
        # (403, "Forbidden: Hopper not cleared for this lane."),
        # (404, "Not Found: Frog missed the lily pad."),
        # (418, "I'm a Teapot: And also a flattened amphibian."),
        # (429, "Too Many Requests: The crosswalk is jammed with turtles."),
        (500, "Internal Server Error: Frogger hit by a memory bus."),
        (502, "Bad Gateway: Log drift caused route misalignment."),
        (503, "Service Unavailable: Arcade machine took a coffee break."),
        (504, "Gateway Timeout: Frog paused mid-hop. Unwise."),
    ]
    code, message = random.choice(errors)

    print(code, message)

    return abort(code, description=message)


@routes.route("/record_question_thumbs_up_down", methods=["POST"])
def record_question_thumbs_up_down():
    player_name = request.headers.get("Player-Name")
    if not player_name:
        raise Exception("No Player Name provided")

    content = request.get_json()

    question = content.get("question", None)
    if not question:
        raise Exception("No question provided")

    question_hash = get_question_hash(question)

    redis = get_redis_conn()

    redis.hsetnx(f"feedback:{question_hash}", "question", question)

    if content.get("is_good", None) is True:
        redis.hincrby(f"feedback:{question_hash}", "count_positive", 1)
    elif content.get("is_bad", None) is True:
        redis.hincrby(f"feedback:{question_hash}", "count_positive", 1)

    return {}
