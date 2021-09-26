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
        # self.update_settings(self.default_settings)
        self.upload_settings()

    def upload_settings(self):
        try:
            with open(constants.WAY_SETTINGS, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.update_settings()

    def update_settings(self, new_settings=default_settings):
        self.settings = new_settings
        with open(constants.WAY_SETTINGS, 'w') as file:
            json.dump(str(self.settings), file)


if __name__ == '__main__':
    s = Settings()
