import string
import random
import jsonhandler as json



def generate_key():
    length = 32
    key = []
    for i in length:
        e=random.randrange(string.ascii_letters,string.digits,string.punctuation)
        key.append(e)
    serverJSON = json.retrieve('server.json')
    count =  0
    for i in serverJSON['auth']:
        count += 1
    serverJSON['auth'][str(count)] = ''.join(key)
    json.commit('server.json',serverJSON)
    print(f'Authkey {key} has been created!')

def banish(key):
    serverJSON = json.retrieve('server.json')
    count = 0    
    for i in serverJSON['auth']:
        count += 1    
        if i == key:
            del serverJSON['auth'][str(count)]
            print(f'Banished {key}')            
            break


