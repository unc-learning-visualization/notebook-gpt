import os
import json
import datetime
from .GPTModel import GPTModel
import NotebookGPT.OnlineLogger as OnlineLogger

class GPTLoggerView():

    def __init__(self, model: GPTModel) -> None:
        self.model = model
        self.log_file = "GPT_Log.json"
        self.makeOrImportLog()

    def makeOrImportLog(self):
        if not os.path.exists(self.log_file):
            base_log =  {
                "timestamp": str(datetime.datetime.now()),
                "log_id": "default", 
                "machine_id": "default",
                "course_id": "default",
                "log": {"interactions":[]}
            }
            with open(self.log_file, "w+") as f: 
                json.dump(base_log, f)
            return base_log
        
        with open(self.log_file, 'r+') as f: 
            return json.load(f)
        
    
    def writeLog(self, new_log):
        with open(self.log_file, "w+") as f: 
                json.dump(new_log, f)

    
    def readLog(self):
        with open(self.log_file, 'r+') as f: 
            return json.load(f)
                
    def updateMetadata(self, old_log):
        notebook_log = self.model.getLog()
        if notebook_log == {}:
            return old_log 
        
        old_log["log_id"] = notebook_log['log_id'] + "_GPT"
        old_log["machine_id"] = notebook_log['machine_id']
        old_log["course_id"] = notebook_log['course_id']
        return old_log

    def updateLog(self, to_add):
        old = self.readLog()
        old['log']['interactions'].append(to_add)

        if old['log_id'] == "default":
            old = self.updateMetadata(old)

        self.writeLog(old)
        OnlineLogger.push_to_cloud(old, "JupyterGPTInteractions")

        
    def transformEvent(self, type, sent, response, problem, raw_input):
        self.updateLog({
            "timestamp": str(datetime.datetime.now()),
            "type": type, 
            "sent": sent,
            "response": response,
            "problem": problem, 
            "raw_input": raw_input
        })


    def update(self, event: dict):
        if event['event'] == "History_GPT":
            self.transformEvent("Generate History Prompt", event['sent'], event['value'], event['problem'], event['raw_input'])
        if event['event'] == "Problem_GPT":
            self.transformEvent("Generate Problem Prompt", event['sent'], event['value'], event['problem'], event['raw_input'])
        if event['event'] == "Sent_GPT":
            self.transformEvent("Sent to GPT", event['sent'], event['value'], event['problem'], event['raw_input'])
