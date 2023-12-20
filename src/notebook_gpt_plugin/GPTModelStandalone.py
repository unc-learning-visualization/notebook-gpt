import random
from .GPTAPI import GPTAPI

class GPTModelStandalone():

    def __init__(self, log_id= "", problem = "", course_id = "default") -> None:
        self.problem = problem
        self.course_id = course_id
        self.log_id = self.generateUniqueId(log_id)
        self.viewers = []
    
    def generateUniqueId(self, log_id_base):
        id = log_id_base
        if log_id_base == "":
            id += "GPTLog"

        id += "-" + str(random.randint(10000000000000000, 99999999999999999))
        return id
    
    def getLogId(self) -> str:
        return self.log_id
    
    def getCourseId(self) -> str: 
        return self.course_id

    def addViewer(self, to_add): 
        self.viewers.append(to_add)

    def update(self, event: dict):
        for i in self.viewers:
            i.update(event)
    
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
        self.update({
            "event":"Enable_Feedback",
        })
        return gpt_response

    def generateCodePrompt(self, to_pass: str):
        response = GPTAPI.generateSinglePrompt(to_pass, self.problem)
        self.update({
            "event":"Single_Code_GPT",
            "value": response,
            "sent": "",
            "raw_input": to_pass,
            "problem": self.problem
        })
        return response
    
    def generateHistoryPrompt(self, history: [str]):
        response = GPTAPI.generateHistoryPrompt(history, self.problem)
        self.update({
            "event":"History_GPT",
            "value": response,
            "sent": "",
            "raw_input": history,
            "problem": self.problem
        })
        return response
    
    def generateProblemPrompt(self):
        response = GPTAPI.generateProblemPrompt(self.problem)
        self.update({
            "event":"Problem_GPT",
            "value": response,
            "sent": "",
            "raw_input": self.problem,
            "problem": self.problem
        })
        return response

    
    def giveFeedback(self, is_positive, sent, response):
        self.update({
            "event":"Student_Feedback",
            "value": response,
            "sent": sent,
            "raw_input": is_positive, 
            "problem": self.problem
        })
    
