import constants
import json


class Score:

    def __init__(self):
        self.score = 0
        try:
            with open('record.json', 'r') as r:
                self.record = json.load(r)
        except FileNotFoundError:
            with open('record.json', 'w') as r:
                json.dump(0, r)
            self.record = 0
        self.x = 25
        self.y = constants.FIELD_HEIGHT * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS - 5

    def update(self, points):
        self.score += points

    def stop_count(self):
        self.score = 0

    def check_record(self):
        if self.score > self.record:
            with open('record.json', 'w') as record_json:
                json.dump(self.score, record_json)
            return True
        return False
