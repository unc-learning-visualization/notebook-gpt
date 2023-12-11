import json
import time
import os
from datetime import datetime
from .GPTAPI import GPTAPI

class GPTModel():

    def __init__(self, log_file, problem) -> None:
        self.log_file = log_file
        self.problem = problem
        self.log = self.getLog()
        self.viewers = []
        self.history = []
    
    def addViewer(self, to_add): 
        self.viewers.append(to_add)

    def update(self, event: dict):
        for i in self.viewers:
            i.update(event)
    
    def refresh(self):
        self.history = self.getCodeHistory()

    def getLog(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r+") as f: 
                return json.load(f)
        return {}
        
    def getLogDiffs(self):
        return self.getLog()['diffs']
    
    def sendToGPT(self, text: str) -> str:
        self.update({
            "event":"Loading",
            "value": "Waiting for ChatGPT to respond...",
        })
        gpt_response, parsed = GPTAPI.sendToGPT(text)
        self.update({
            "event":"Sent_GPT",
            "value": gpt_response,
            "sent": parsed,
            "raw_input": text,
            "problem": self.problem
        })

    def generateCodePrompt(self):
        to_pass = ""
        if len(self.history) > 0:
            to_pass = self.history[0]
        
        response = GPTAPI.generateSinglePrompt(to_pass, self.problem)
        self.update({
            "event":"Single_Code_GPT",
            "value": response,
            "sent": "",
            "raw_input": to_pass,
            "problem": self.problem
        })
    
    def generateHistoryPrompt(self):
        response = GPTAPI.generateHistoryPrompt(self.history, self.problem)
        self.update({
            "event":"History_GPT",
            "value": response,
            "sent": "",
            "raw_input": self.history,
            "problem": self.problem
        })
    
    def generateProblemPrompt(self):
        response = GPTAPI.generateProblemPrompt(self.problem)
        self.update({
            "event":"Problem_GPT",
            "value": response,
            "sent": "",
            "raw_input": self.problem,
            "problem": self.problem
        })
    
    def getCodeHistory(self, max_size=5) -> [str]:
        diffs = self.getLogDiffs()
        times = []
        keeper= {}
        for i in diffs:
            convert = formatTime(i['time'])
            times.append(convert)
            keeper.update({convert:i['time']})
        times.sort(reverse=True)
        keep = times[0:max_size*2]
        keepString = [keeper[x] for x in keep]
        kept = [x for x in diffs if x['time'] in keepString]
        kept = GPTModel.__OrderDiffs(keep, keeper, kept)
        history = GPTModel.__buildHistory(kept, max_size)
        self.update({
            "event":"History_Response",
            "value": history
        })
        return history
    
    @staticmethod
    def __OrderDiffs(correctOrder, keeperDict, unOrderedArray):
        new_list = []
        for i in correctOrder:
            stamp = keeperDict[i]
            for j in unOrderedArray:
                if j['time'] == stamp:
                    new_list.append(j)
        return new_list 

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
            
            full_string = "Timestamp: " + timepoint['time'] + '\n'
            if 'source' in new_content:
                full_string = GPTModel.__buildCodeString(new_content['source'], full_string)
            if 'outputs' in new_content:
                for i in new_content['outputs']:
                    if i['output_type'] == 'stream':
                        full_string = GPTModel.__buildStdOutString(full_string, i)
                    if i['output_type'] == 'error':
                        full_string = GPTModel.__buildErrorString(full_string, i)
            
            to_return.append(full_string)

        if len(to_return) > max_size:
            to_return = to_return[0:max_size]
        return to_return

    @staticmethod
    def __buildCodeString(source_array: [str], current_string):
        current_string += "Code: \n```\n"
        for i in source_array:
            current_string += i 
        return current_string + '\n```\n'
    
    @staticmethod
    def __buildStdOutString(current, new):
        current += "\nStandard Output:\n"
        for i in new['text']:
            current += i 
        return current + '\n'
    
    @staticmethod 
    def __buildErrorString(current, new):
        current += "\nError Output:\n"
        current += "Error Name: " + new['ename'] + "\nTraceback:\n"
        for i in new['traceback']:
            current += i
        return current + '\n'
    
def formatTime(dateString):
    date = ""
    try:
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S.%f")
    except:
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
    return date
