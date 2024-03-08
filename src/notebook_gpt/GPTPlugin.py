from .OnlineLogger import start
import ipynbname
from .GPTModel import GPTModel
from .GPTView import GPTView
from .GPTLoggerView import GPTLoggerView


def GPTPlugin(unique_id="GPT-User", course_taken="GPT-Course", problem="", notebook_name="", consent=True ):
    if not consent:
        print("You must allow logging to use this plugin!")
        return
    
    if notebook_name == "":
        notebook_name = ipynbname.name() + ".ipynb"
    
    base_id = unique_id + "-"
    log_file = notebook_name.split('.ipynb')[0] + "_log.json"
    model = GPTModel(log_file, problem)
    start(notebook_name, course_taken, base_id, model=model)
    view = GPTView(model)
    gptLogger = GPTLoggerView(model)
    model.addViewer(view)
    model.addViewer(gptLogger)
    view.displayWidget()
    
