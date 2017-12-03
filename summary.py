#summary python code
import Algorithmia

#returns string of summary, 3 sentences
def getSummary(input):
    client = Algorithmia.client('simb6+Jq53ctwOjKQMx9LNNtvkH1')
    algo = client.algo('nlp/Summarizer/0.1.6')
    a=algo.pipe(input)
    return a.result
