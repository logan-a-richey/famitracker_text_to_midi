# track.py

class Track:
    def __init__(self):
        self.name = ""
        self.speed = 6
        self.tempo = 150
        self.num_rows = 64
        self.num_cols = 5
        self.eff_cols = [1 for _ in range(5)]

        self.orders = {}
        self.tokens = {}
