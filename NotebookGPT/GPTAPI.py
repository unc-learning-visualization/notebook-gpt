

class GPTAPI():

    @staticmethod
    def sendToGPT(text: str):
        print(text)
        return {}
    
    @staticmethod 
    def sendHistoryToGPT(codeHistory: [str]):
        for i in codeHistory:
            print(i)
        return {}