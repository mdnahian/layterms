import requests
import json
import pdb
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

entityNames = [
'individual',
'business customer',
'information',
'personally identifiable information',
'providers',
'acknowledgement',
'ip address',
'interest',
'arrow',
'web sites',
'privacy statement',
'apps',
'responsibility',
'solutions',
'products',
'parties',
'users',
'device',
'faq',
'borders',
'data',
'market',
'relationship',
'contributions',
]

currGraphValues = {}

def getEntity(text):
    api_url = 'https://language.googleapis.com/v1/documents:annotateText?key=AIzaSyDZUZaUB5Oz52iTRk4KYYNjqGtV6XLXEV8'
    entityData = {
    'document':{'type':'PLAIN_TEXT','content':text},
    'features':{
      "extractSyntax": False,
      "extractEntities": True,
      "extractDocumentSentiment": False,
      "extractEntitySentiment": False,
      "classifyText": False,
    },
    'encodingType':'UTF8'
    }
    response = requests.post(api_url, json.dumps(entityData))
    return json.loads(response.text)

def getSalience(jsonData):
    jsonData = jsonData['entities']
    for i,currE in enumerate(jsonData):
        if currE['name'] in entityNames:
            print('wa')
            currGraphValues[currE['name']]=jsonData[i]['salience']

# Main
f = open('Corpus/Input/craigslist_policy.txt')
txt = f.readlines()
txt = '\n'.join(txt)

jsonData = getEntity(txt)
getSalience(jsonData)

# Open Image
source_img = Image.open('insight_graph.png').convert("RGBA")
draw = ImageDraw.Draw(source_img)

for key in currGraphValues.keys():
    size = 3
    index = entityNames.index(key)

    x_center = 135+54*index
    y_center = -566*currGraphValues[key]+578

    draw.rectangle(((x_center-size, y_center-size), (x_center+size, y_center+size)), fill="red")

source_img.save('currentInsightGraph.png', "PNG")
