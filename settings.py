
class Settings:
    def __init__(self, win_width = 500, win_height = 500):
        # width and height are swaped / cant fix right now
        # doesnt work when win_width != win_height
        self.win_width = win_width
        self.win_height = win_height

    def change_win_width_height(self, win_width = 0, win_height = 0):
        if win_width == 0 and win_height == 0:
            return 0

        if win_width != 0:
            self.win_width = win_width

        if win_height != 0:
            self.win_height = win_height
        
        return 1

_settings = Settings()