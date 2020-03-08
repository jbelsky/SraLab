class Friend:

    def __init__(self, _id):

        self.id = _id
        self.top3 = False
        self.closest = False

    def set_top3(self):
        self.top3 = True

    def set_closest(self):
        self.closest = True

    def is_top3(self):
        return self.top3

    def is_closest(self):
        return self.closest