class Word:

    def __init__(self, word, index, visited):
        self.index = index
        self.correct = None
        self.visited = visited
        self.word = word
        self.color = (171, 171, 171)
        self.current = False

    def get_index(self):
        return self.index

    def get_color(self):
        if self.visited:
            if self.correct:
                self.color = (126, 173, 105)
            else:
                self.color = (199, 17, 80)
        else:
            if self.current:
                self.color = (255, 255, 255)
        return self.color


