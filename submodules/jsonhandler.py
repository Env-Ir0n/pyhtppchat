import json

def commit(jsonfile,dict):
    to_commit = dict
    commit_to = jsonfile
    with open(commit_to,'w') as f:
        f.write(json.dumps(to_commit))
    print(f'Commited to {jsonfile}')

def retrieve(jsonfile):
    print(f'{jsonfile} has been retrieved')
    return json.loads(jsonfile)
    
def isthere(tosearch,dict):
    for keys in dict:
        if dict[keys] == tosearch:
            return True
        else:
            return False

#this is here so i dont have to import json as well as jsonhandler
        
def dumps(content):
    return json.dumps(content)

def dump(content):
    return json.dump(content)

