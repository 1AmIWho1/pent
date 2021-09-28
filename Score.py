import constants
import json


class Score:

    def __init__(self):
        self.score = 0
        self.solved = 0
        try:
            with open(constants.WAY_RECORD, 'r') as r:
                self.record = json.load(r)
        except FileNotFoundError:
            with open(constants.WAY_RECORD, 'w') as r:
                json.dump(0, r)
            self.record = 0

    def update(self, points):
        self.score += points

    def solve(self):
        self.solved += 1

    def stop_count(self):
        self.score = 0

    def check_record(self):
        if self.score > self.record:
            with open(constants.WAY_RECORD, 'w') as record_json:
                json.dump(self.score, record_json)
            return True
        return False
