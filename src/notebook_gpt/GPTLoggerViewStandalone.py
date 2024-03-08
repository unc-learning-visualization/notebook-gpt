import os
import json
import datetime
from .GPTModelStandalone import GPTModelStandalone
from .OnlineLogger import push_to_cloud

class GPTLoggerViewStandalone():

    def __init__(self, model: GPTModelStandalone) -> None:
        self.model = model
        self.log_file = self.model.getLogId() + "_GPT" + ".json"
        self.makeOrImportLog()

    def makeOrImportLog(self):
        if not os.path.exists(self.log_file):
            base_log =  {
                "timestamp": str(datetime.datetime.now()),
                "log_id": self.model.getLogId() + "_GPT",
                "machine_id": "default",
                "course_id": self.model.getCourseId(),
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

    def updateLog(self, to_add):
        old = self.readLog()
        old['log']['interactions'].append(to_add)

        self.writeLog(old)
        push_to_cloud(old, "StandaloneGPTInteractions")

        
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
        if event['event'] == "Single_Code_GPT":
            self.transformEvent("Generate Code Prompt", event['sent'], event['value'], event['problem'], event['raw_input'])
        if event['event'] == "Sent_GPT":
            self.transformEvent("Sent to GPT", event['sent'], event['value'], event['problem'], event['raw_input'])
        if event['event'] == "Student_Feedback": 
            self.transformEvent("Student GPT Response Feedback", event['sent'], event['value'], event['problem'], event['raw_input'])

