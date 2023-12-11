

import requests
import json
import os
import re
from dotenv import load_dotenv

class GPTAPI():

    @staticmethod
    def handleChoice(choice_object) -> str:
        to_return = ""
        
        if 'message' not in choice_object:
            return "No ChatGPT message returned."
        message_object = choice_object['message']

        if 'content' not in message_object:
            return "No ChatGPT message returned."

        raw_return = message_object['content']
        raw_code_array = raw_return.split("```")

        val = 0
        return_array = []
        for section in raw_code_array:
            if val % 2 != 0:
                return_array.append("<CODE REDACTED>") 
                val += 1
                continue 
            return_array.append(section)
            val += 1
            
        return "".join(return_array)

    @staticmethod
    def cleanText(text: str):
        to_return = re.sub(r"\n[\t' ']*\n", "\n", text)
        if to_return[-1] == "\n":
            to_return = to_return[:-1]
        return to_return
            

    @staticmethod
    def sendToGPT(text: str):
        load_dotenv()
        
        url = "https://us-east-1.aws.data.mongodb-api.com/app/rest-api-vsfoo/endpoint/gpt_request?secret=" + os.getenv("API_SECRET")

        text = GPTAPI.cleanText(text)
        payload = json.dumps({
          "text": text
        })
        headers = {
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            return response.json()['message'], text

        parse = response.json()

        if 'choices' in parse and len(parse['choices']) != 1: 
            return "Chat does not currently support choices. Please ask a question that will likely give a single answer."

        return GPTAPI.handleChoice(parse['choices'][0]), text
    
    @staticmethod
    def generateHistoryPrompt(history: [str], problem: str) -> str:
        base = GPTAPI.generateProblemPrompt(problem)
        base += "I am stuck on my code and would like advice on how to solve my problem.\n"
        base += "I am going to send you a history of my recent code with the following format:\n"
        base += "Timestamp: <Timestamp>\n"
        base += "Code:\n <The Code At That Timestamp>\n"
        base += "Standard Output:\n <The codes standard output>\n"
        base += "Error Output:\n Error Name: <Name of the error in the programming language>\n"
        base += "<The error output of the code>\n"
        base += "This pattern will repeat for some number of timepoints. Some sections may be missing.\n"
        base += "What advice would you give based on the following history:\n"
        for i in history:
            base += i
        return base
    
    @staticmethod
    def generateProblemPrompt(problem: str) -> str: 
        resp = "Imagine you are a tutor for a programming class and the student comes to you for help.\n"
        resp += "You should not give them code in your responses and instead, you should guide them to an answer or help them in natural language.\n"
        if problem != "":
            resp += "In addition, they are working on a problem with the prompt: " + problem + "\n"
        
        
        resp += "The student then asks the following question:\n"
        
        return resp