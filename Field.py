import constants


class Field:  # model

    def __init__(self):
        self.field = [[False for i in range(constants.FIELD_WIDTH)] for i in range(constants.FIELD_HEIGHT)]
        self.color_stopped_figures = constants.COLORS['STOP_COLOR']
