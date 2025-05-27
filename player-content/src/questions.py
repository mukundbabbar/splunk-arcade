import json
import os
from random import randint

from redis import StrictRedis

SPLUNK_OBSERVABILITY_REALM = os.getenv("SPLUNK_OBSERVABILITY_REALM", "us1")
MAX_QUESTION_SELECTION_ATTEMPTS = 5
# Currently us1 points to a dashboard in Show Playground. 
#!!!!!!! UPDATE THESE DASHBOARDS TO THE CORRECT ORGS ONCE DECIDED !!!!!!!!!
ARCADE_O11Y_DASHBOARD = {"us1":"Grko8cDA0Ao?groupId=GjETzI8AwAE&startTime=-1h&endTime=Now", "eu0":"placeHolDeERid?groupId=PlAcEHoLDeRid"}


class _Questions:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        self.f = open("questions.json", mode="r")
        self.content = json.load(self.f)
        self.redis = StrictRedis(
            host=os.getenv("REDIS_HOST", "cache"),
            port=6379,
            db=0,
            decode_responses=True,
        )

    def questions_for_module(  # noqa: C901
        self, module: str, question_count: int, seen_questions: list[str], player_name: str
    ) -> list[dict]:
        _module = module.lower()

        if _module not in self.content:
            raise Exception(f"module '{module}' is not in questions bank")

        fixed_questions = self.content.get(_module, {}).get("fixed_order", [])
        fixed_counter = 0
        iters = 0
        out_questions = []

        while True:
            maybe_question = None

            if (len(seen_questions) + fixed_counter) < len(fixed_questions):
                maybe_question = fixed_questions[len(seen_questions) + fixed_counter]
                fixed_counter += 1
            elif (len(seen_questions) + len(out_questions)) < len(fixed_questions) + len(
                self.content[module]["other"]
            ):
                while True:
                    maybe_question = self.content[module]["other"][
                        randint(0, len(self.content[module]) - 1)
                    ]
                    if maybe_question["question"] not in seen_questions:
                        break

            if maybe_question and maybe_question["question"] not in seen_questions:
                maybe_question["question"] = maybe_question["question"].replace(
                    "__PLAYER_NAME__", player_name
                )
                if "link" in maybe_question:
                    maybe_question["link"] = maybe_question["link"].replace(
                        "__PLAYER_NAME__", player_name
                    )
                    maybe_question["link"] = maybe_question["link"].replace(
                        "__REALM__",
                        SPLUNK_OBSERVABILITY_REALM,
                    )
                    maybe_question["link"] = maybe_question["link"].replace(
                            "__DASHBOARD__",
                            ARCADE_O11Y_DASHBOARD.get(SPLUNK_OBSERVABILITY_REALM, "Grko8cDA0Ao?groupId=GjETzI8AwAE")
                    )

                out_questions.append(maybe_question)

            if len(out_questions) >= question_count:
                return out_questions

            iters += 1

            if iters > MAX_QUESTION_SELECTION_ATTEMPTS:
                # couldnt find all the questions requested, if we have some, ship em otherwise
                # just return an empty list for front end to deal with
                if out_questions:
                    return out_questions
                return []
