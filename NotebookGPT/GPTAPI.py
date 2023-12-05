

class GPTAPI():

    @staticmethod
    def sendToGPT(text: str, problem: str):
        return str(text + problem), "sample"
    
    @staticmethod 
    def sendHistoryToGPT(codeHistory: [str], problem: str):
        return ".".join(codeHistory), "sample"