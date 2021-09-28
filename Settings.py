import json
import os
import constants


class Settings:

    default_settings = {
        'field_width': constants.FIELD_WIDTH,
        'field_height': constants.FIELD_HEIGHT,
        'grid': constants.GRID,
        'stop_color': constants.STOP_COLOR,
    }

    def __init__(self):
        self.settings = self.default_settings
        self.window_width = self.settings['field_width'] * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH
        self.window_height = self.settings['field_height'] * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS
        self.upload_settings()

    def upload_settings(self):
        try:
            with open(constants.WAY_SETTINGS, 'r') as file:
                data = json.load(file)
                if data.keys() == self.default_settings.keys():
                    self.update_settings(data)
                else:
                    self.update_settings()
        except FileNotFoundError:
            self.update_settings()

    def update_settings(self, new_settings=default_settings):
        self.settings = new_settings
        self.window_width = self.settings['field_width'] * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH
        self.window_height = self.settings['field_height'] * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS
        with open(constants.WAY_SETTINGS, 'w') as file:
            json.dump(self.settings, file)


if __name__ == '__main__':
    s = Settings()
