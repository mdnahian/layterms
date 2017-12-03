import requests
import json
import pdb

# Opening file and reading policy
currWebsite = 'twitter'
f = open('Corpus/'+currWebsite+'_policy.txt','r')
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
f = open('Corpus/'+currWebsite+'_raw.txt','w+')
f.write(response.text)
f.close()

# Google Cloud API for
