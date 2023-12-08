

class GPTAPI():

    @staticmethod
    def sendToGPT(text: str):
        return text
    
    @staticmethod
    def generateHistoryPrompt(history: [str], problem: str) -> str:
        return "history"
    
    @staticmethod
    def generateProblemPrompt(problem: str) -> str: 
        return "problem"