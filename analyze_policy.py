import re
import json

class Policy:
    def __init__(self, service, text):
        self.service = service 
        self.text = text # should be list of paragraphs with headings

collection_keywords = ['get', 'gets', 'getting',
                       'collect', 'collects', 'collecting',
                       'use', 'uses', 'using',
                       'receive', 'receives', 'receiving',
                       'log', 'logs', 'logging',
                       'record,' 'records', 'recording',
                       'give', 'gives', 'giving',
                       'store', 'stores', 'storing',
                       'obtain', 'obtains', 'obtaining',
                       'provide', 'provides', 'providing'
                       ]

neg_keywords = ['do not', 'does not', 'will not', 'never', 'will never', 'won\'t', 'doesn\'t']

info_types = {'name':
                ['name'],
              'birthdate':
                ['birthday', 'date of birth', 'birth date', 'day of birth', 'year of birth'],
              'address':
                ['home address', 'your address', 'postal address', 'shipping address', 'billing address', ', address'],
              'phone number':
                ['phone number', 'mobile number', 'home number', 'telephone number'],
              'email address':
                ['email address', 'e-mail address'],
              'payment information':
                ['payment information', 'payment details', 'payment data', 'financial information', 'bank account number', 'bank account numbers', 'card number', 'card numbers', 'credit card information', 'debit card information', 'bank account information'],
              'SSN':
                ['SSN', 'social security number', 'social security numbers'],
              'IP address':
                ['IP address', 'IP addresses', ' IP ', 'Internet Protocol'],
              'browser':
                ['browser type', 'type of browser'],
              'device':
                ['device type', 'type of device'],
              'accelerometer':
                ['accelerometer'],
              'gyroscope':
                ['gyroscope'],
              'GPS':
                ['GPS'],
              'microphone':
                ['microphone'],
              'camera':
                ['camera'],
              'photos':
                ['photos'],
              'contacts':
                ['contacts'],
              'gender':
                ['gender'],
              'third party login credentials':
                [],
              'third party account information':
                [],
              'service provider':
                ['service provider'],
              'cookies':
                ['cookie', 'cookies'],
              'web beacons':
                ['beacons', 'beacon', 'web beacons', 'web beacon', 'tracker pixel', 'tracker pixels'],
              'network connection type':
                [],
              'operating system':
                ['operating system'],
              'language':
                ['language'],
              'previous url':
                [],
              'next url':
                [],
              'interactions with ad':
                []
              }


entities = {'advertisers':
                ['advertisers', 'customize the advertising', 'targeted ad', 'targeted ads', 'tailored ad'],
            'corporate affiliates':
                ['affiliat', 'family of companies'],
            'authorities':
                ['authorities', 'law', 'government'],
            'social media you log in with':
                ['social media you log in with'],
            'service providers':
                ['service providers']
              }


def do_they_collect(data, info_type):
    data = data.lower()
    sentences = re.findall(r"([^.]*\.)", data)
    for sentence in sentences:
        for c_keyword in collection_keywords:
            for i_keyword in info_types[info_type]:
                if c_keyword.lower() in sentence and i_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                    return True
    return False

def can_see_info(entity):
    data = data.lower()
    sentences = re.findall(r"([^.]*\.)", data)
    sharing_keywords = collection_keywords + ['share', 'shares', 'sharing', 'disclose', 'discloses', 'disclosing']
    if entity == 'advertisers':
        for sentence in sentences:
            for s_keyword in sharing_keywords:
                for a_keyword in ['advertis', 'ads']:
                    for t_keyword in ['target', 'tailor', 'customiz', 'personaliz']:
                        if s_keyword.lower() in sentence and a_keyword.lower() in sentence and t_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                            return True
        return False
    else:
        for sentence in sentences:
            for s_keyword in sharing_keywords:
                for e_keyword in entities[entity]:
                    if s_keyword.lower() in sentence and e_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                        return True
        return False

def analyze(company, policy):
    info_dict = {}
    with open(policy, 'r', encoding='utf8') as textfile:
        data = textfile.read().replace('\n', '')
        for info_type in info_types:
            info_dict[info_type] = do_they_collect(data, info_type)
    return info_dict

tdict = analyze('Twitter', 'policies/twitter_policy.txt')
print(json.dumps(tdict))



