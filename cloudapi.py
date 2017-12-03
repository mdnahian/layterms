import requests
import json
import pdb

# Opening file and reading policy
currWebsite = 'twitter'
f = open('Corpus/'+currWebsite+'.policy','r')
text=f.readlines()
text='\n'.join(text)
f.close()

# Google Cloud API
api_url = 'https://language.googleapis.com/v1/documents:analyzeSyntax?key=AIzaSyDZUZaUB5Oz52iTRk4KYYNjqGtV6XLXEV8'

entityData = {'document':{'type':'PLAIN_TEXT','content':text},'encodingType':'UTF8'}

response = requests.post(api_url, json.dumps(entityData))

# Writing response
f = open('Corpus/'+currWebsite+'.raw','w+')
f.write(response.text)
f.close()
