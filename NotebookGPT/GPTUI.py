from .GPTModel import GPTModel
from .GPTView import GPTView

class GPTUI: 

    def __init__(self, log_file) -> None:
        self.log_file = log_file

    def start(self):
        model = GPTModel(self.log_file)
        view = GPTView(model)
        view.display()