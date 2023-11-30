from .GPTModel import GPTModel

class GPTView():

    def __init__(self, model: GPTModel) -> None:
        self.model = model

    def display(self):
        hist = self.model.getCodeHistory()
        print(hist)