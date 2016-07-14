class StringCursor:
    def __init__(self, string):
        self.string = string
        self.cursor = 0

    def end(self):
        return self.cursor == len(self.string)

    def read(self):
        return self.string[self.cursor:]

    def read_one(self):
        return self.string[self.cursor]

    def increment(self, distance=1):
        self.cursor += distance
