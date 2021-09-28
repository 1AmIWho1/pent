import constants


class Menu:

    def __init__(self, buttons={}, input_boxes={}):
        self.sentence = 'Waiting'
        self.buttons = buttons
        self.input_boxes = input_boxes

    def update(self):
        for input_box in self.input_boxes.values():
            input_box.stop_input()
