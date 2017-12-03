import re
import json

collection_keywords = ['get', 'gets', 'getting',
                       'collect', 'collects', 'collecting',
                       'use', 'uses', 'using',
                       'receive', 'receives', 'receiving',
                       'log', 'logs', 'logging',
                       'record,' 'records', 'recording',
                       'give', 'gives', 'giving',
                       'store', 'stores', 'storing',
                       'obtain', 'obtains', 'obtaining',
                       'provide', 'provides', 'providing',
                       'access', 'accesses', 'accessing'
                       ]

neg_keywords = ['do not', 'does not', 'will not', 'never', 'will never', 'won\'t', 'doesn\'t']

info_types = {'Name':
                ['your name'],
              'Birthdate':
                ['birthday', 'date of birth', 'birth date', 'day of birth', 'year of birth'],
              'Address':
                ['home address', 'your address', 'postal address', 'shipping address', 'billing address', ', address'],
              'Phone number':
                ['phone number', 'mobile number', 'home number', 'telephone number'],
              'Email address':
                ['email address', 'e-mail address'],
              'Payment information':
                ['payment information', 'payment details', 'payment data', 'financial information', 'bank account number', 'bank account numbers', 'card number', 'card numbers', 'credit card information', 'debit card information', 'bank account information'],
              'SSN':
                ['SSN', 'social security number', 'social security numbers'],
              'IP address':
                ['IP address', 'IP addresses', ' IP ', 'Internet Protocol'],
              'Browser':
                ['browser type', 'type of browser'],
              'Device':
                ['device type', 'type of device'],
              'Accelerometer':
                ['accelerometer'],
              'Gyroscope':
                ['gyroscope'],
              'GPS':
                ['GPS'],
              'Microphone':
                ['microphone'],
              'Camera':
                ['camera'],
              'Photos':
                ['photos'],
              'Contacts':
                ['contacts'],
              'Gender':
                ['gender'],
              'Cookies':
                ['cookie', 'cookies'],
              'Web beacons':
                ['beacon', 'tracker pixel'],
              'Operating system':
                ['operating system'],
              'Site you came from':
                ['referral URL', 'clickstream', 'referrer URL', 'referring site', 'referrer site', 'referral site', 'referring page', 'referring URL', 'exit page', 'exit URL', 'site you came from', 'site you go to next', 'that referred you']
              }


entities = {'Advertisers':
                ['advertisers', 'customize the advertising', 'targeted ad', 'targeted ads', 'tailored ad'],
            'Corporate affiliates':
                ['affiliat', 'family of companies', 'parent corporation', 'parent company', 'subsidiary', 'subsidiaries', 'corporate family'],
            'Authorities':
                ['authorities', 'law', 'government'],
            'Service providers':
                ['service provider']
              }


def do_they_collect(data, info_type):
    sentences = re.findall(r"([^.]*\.)", data)
    for sentence in sentences:
        for c_keyword in collection_keywords:
            for i_keyword in info_types[info_type]:
                if c_keyword.lower() in sentence.lower() and i_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                    return True, sentence
    return False, None

def can_see_info(data, entity):
    sentences = re.findall(r"([^.]*\.)", data)
    sharing_keywords = collection_keywords + ['share', 'shares', 'sharing', 'disclose', 'discloses', 'disclosing']
    if entity == 'advertisers':
        for sentence in sentences:
            for s_keyword in sharing_keywords:
                for a_keyword in ['advertis', 'ads']:
                    for t_keyword in ['target', 'tailor', 'customiz', 'personaliz']:
                        if s_keyword.lower() in sentence and a_keyword.lower() in sentence.lower() and t_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                            return True, sentence
        return False, None
    else:
        for sentence in sentences:
            for s_keyword in sharing_keywords:
                for e_keyword in entities[entity]:
                    if s_keyword.lower() in sentence.lower() and e_keyword.lower() in sentence and all(negative not in sentence for negative in neg_keywords):
                        return True, sentence
        return False, None

def analyze(policy):
    info_array = []
    entity_array = []

    data = policy.encode('utf-8').replace('\n', '')
    for info_type in info_types:
        info_array.append([info_type] + list(do_they_collect(data, info_type)))
    for entity in entities:
        entity_array.append([entity] + list(can_see_info(data, entity)))
    return info_array, entity_array

# print(analyze('policies/twitter_policy.txt'))
