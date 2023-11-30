import NotebookGPT.OnlineLogger as OnlineLogger
from .GPTUI import GPTUI
import ipynbname
import json


def GPTPlugin(unique_id="GPT-User", course_taken="GPT-Course", notebook_name=""):
    if notebook_name == "":
        notebook_name = ipynbname.name() + ".ipynb"
    
    base_id = unique_id + "-"
    log_file = notebook_name.split('.ipynb')[0] + "_log.json"
    OnlineLogger.start(notebook_name, course_taken, base_id)
    UI = GPTUI(log_file)
    UI.start()
    
