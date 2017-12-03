class Policy:
    def __init__(self, service, text):
        self.service = service 
        self.text = text # should be list of paragraphs with headings

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
              'mobile service provider':
                [],
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

def do_they_collect(data, info_type):
    return bool(sum([data.lower().count(x.lower()) for x in info_types[info_type]]))

def is_use_used(use):
    pass

def can_see_info(entity):
    pass

def analyze(company, policy):
    info_dict = {}
    with open(policy, 'r', encoding='utf8') as textfile:
        data = textfile.read().replace('\n', '')
        for info_type in info_types:
            info_dict[info_type] = do_they_collect(data, info_type)
    return company, info_dict

print(analyze('Stripe', 'stripe_policy.txt'))


