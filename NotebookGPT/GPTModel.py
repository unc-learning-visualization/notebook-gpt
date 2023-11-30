import json
from datetime import datetime
from .GPTAPI import GPTAPI

class GPTModel():

    def __init__(self, log_file) -> None:
        self.log_file = log_file

    
    def getLog(self):
        with open(self.log_file, "r+") as f: 
            return json.load(f)
        
    def getLogDiffs(self):
        return self.getLog()['diffs']
    
    def sendToGPT(self, text: str):
        return GPTAPI.sendToGPT(text)
    
    def sendCodeHistoryToGPT(self, history: [str]):
        return GPTAPI.sendHistoryToGPT(history)
    
    def getCodeHistory(self, max_size=5) -> [str]:
        diffs = self.getLogDiffs()
        times = []
        for i in diffs:
            times.append(i['time'])
        times.reverse()
        keep = times[0:max_size*2]
    
        kept = [x for x in diffs if x['time'] in keep]
        return GPTModel.__buildHistory(kept, max_size)
    
    @staticmethod
    def __buildHistory(kept, max_size):
        to_return = []
        cell_to_monitor = -1
        for timepoint in kept:
            cells_changed = timepoint['cells_changed']
            
            # Return what has changed so far. 
            if len(cells_changed) == 0: 
                return to_return
            
            # Find cell to monitor if not found already
            if cell_to_monitor == -1: 
                cell_to_monitor = max(cells_changed)

            if cell_to_monitor not in cells_changed:
                continue 

            position = cells_changed.index(cell_to_monitor)
            new_content = timepoint['new_contents'][position]
            full_string = ""
            if 'source' in new_content:
                full_string = GPTModel.__buildCodeString(new_content['source'])
 
            if 'outputs' in new_content:
                for i in new_content['outputs']:
                    if i['output_type'] == 'stream':
                        print("std")
                        full_string = GPTModel.__buildStdOutString(full_string, i)
                    if i['output_type'] == 'error':
                        print("error")
                        full_string = GPTModel.__buildErrorString(full_string, i)
            
            to_return.append(full_string)

        if len(to_return) > max_size:
            to_return = to_return[0:max_size]
        return to_return

    @staticmethod
    def __buildCodeString(source_array: [str]):
        current_string = "Code: \n"
        for i in source_array:
            current_string += i 
        return current_string
    
    @staticmethod
    def __buildStdOutString(current, new):
        current += "\nStandard Output:\n"
        for i in new['text']:
            current += i 
        return current
    
    @staticmethod 
    def __buildErrorString(current, new):
        current += "\nError Output:\n"
        current += "Error Name: " + new['ename'] + "\nTraceback:\n"
        for i in new['traceback']:
            current += i
        return current
    
def formatTime(dateString):
    date = ""
    try:
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S.%f")
    except:
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
    return date
