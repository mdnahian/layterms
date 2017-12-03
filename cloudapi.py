import requests
import json
import pdb
import os

fileList = os.listdir('Corpus/Input/')
# Opening file and reading policy
for currFile in fileList:
    currWebsite = currFile.split('.')[0].split('_')[0]
    f = open('Corpus/Input/'+currWebsite+'_policy.txt','r')
    text=f.readlines()
    text='\n'.join(text)
    f.close()

    # Google Cloud API for entities
    api_url = 'https://language.googleapis.com/v1/documents:annotateText?key=AIzaSyDZUZaUB5Oz52iTRk4KYYNjqGtV6XLXEV8'

    entityData = {
    'document':{'type':'PLAIN_TEXT','content':text},
    'features':{
      "extractSyntax": True,
      "extractEntities": True,
      "extractDocumentSentiment": True,
      "extractEntitySentiment": True,
      "classifyText": True,
    },
    'encodingType':'UTF8'
    }

    response = requests.post(api_url, json.dumps(entityData))

    # Writing entity response
    f = open('Corpus/Output/'+currWebsite+'_raw.txt','w+')
    f.write(response.text)
    f.close()
