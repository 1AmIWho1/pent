import constants


class Menu:

    def __init__(self, buttons={}, input_boxes={}):
        self.sentence = 'Waiting'
        self.buttons = buttons
        self.input_boxes = input_boxes

    def save_settings(self):
        pass
