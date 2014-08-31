import json,yaml,builtinext,praw

with open('.auth.json') as f:
    auth = json.load(f,object_hook=builtinext.AttrDict)

# Blurred dataset

with open('blurred.yaml') as f:
    dataset = yaml.load(f)
