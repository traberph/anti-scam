import requests
from fake_useragent import UserAgent
import faker
import csv
import random
import os

url = 'https://janjboer.nl/1000/say.php'
#url = 'http://localhost:8080'

matomo = 'https://s.traberph.de/matomo.php'
site_id = '1'

ua = UserAgent()
fake = faker.Faker(['de_DE', 'en_US'])

# load password list
with open('pwd.csv') as f:
    reader = csv.reader(f)
    pwd_list = list(reader)


# send request
def send():
    header = {'User-Agent': str(ua.random)}
    form_data = {
        'Username': get_email(),
        'Password': get_password()
    }
    response = requests.post(url, data=form_data, headers=header)


    # prospone console output if MUTE is set
    if os.getenv('MUTE') is None:
        print(f'send: {response.request.body}, received: {response.status_code}', flush=True)

    return response.status_code


# fake emails
def get_email():
    fst = fake.first_name().lower()
    sec = fake.last_name().lower()
    return f'{fst}.{sec}@uni-konstanz.de'


# fake passwords

def get_from_list():
    return random.choice(pwd_list)[1]

def generate():
    return fake.password(random.randint(10, 26))

def get_password():
    return generate() if random.choice([True, False, False, False]) else get_from_list()



def send_stats(stats):

    # Construct the payload
    payload = {
        'idsite': site_id,
        'url': 'uni spam',
        'rec': 1,
        'rand': random.randint(0, 100000),
    } 

    for status_code, count in stats.items():
        payload[f'dimension{status_code}'] = count

    # Send the tracking request
    response = requests.get(matomo, params=payload)
    return response.status_code
    


# main loop

result = {}
counter = 0
print(f'this program will send requests to {url}', flush=True)
while True:
    try:
        code = send()
        try:
            c = int(code/100)
        except:
            c = 1
    except Exception as e:
        print(e)
        c = 1
    result[c] = result.get(c, 0) + 1
    counter += 1

    if counter >= 25:
        print('---')
        print(result)
        print(send_stats(result))
        print('---')
        counter = 0
        result = {}