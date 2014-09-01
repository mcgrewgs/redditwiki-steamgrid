import json,yaml,builtinext,praw,requests,time,warnings

warnings.filterwarnings("ignore")

with open('.auth.json') as f:
    auth = json.load(f,object_hook=builtinext.AttrDict)

def mapreplace(loader,node):
    return builtinext.AttrDict(loader.construct_mapping(node))
yaml.add_constructor(u'tag:yaml.org,2002:map',mapreplace)


#listgrabber
def imgur(album):
    headers = auth.imgur
    response = requests.get("https://api.imgur.com/3/album/{}".format(album),headers=headers)
    response.raise_for_status()
    time.sleep(2)
    return list(map(lambda x:x.title,response.json(object_hook=builtinext.AttrDict).data.images))



# Blurred dataset

with open('blurred.yaml') as f:
    dataset = yaml.load(f)

for item in dataset:
    print("### /u/{}".format(item.name))
    if 'albums' in item:
        ids = map(lambda x:"http://imgur.com/a/"+x.id,item.albums)
        print("Albums: {}  ".format(', '.join(ids)))
    if 'threads' in item:
        ids = map(lambda x:"http://redd.it/"+x,item.threads)
        print("Threads: {}  ".format(', '.join(ids)))
    if 'images' in item:
        print("Images: {}  ".format(','.join(item.images)))
    
    print()

    #games list
    if not 'games' in item:
        item.games = []
    if 'albums' in item:
        for album in item.albums:
            if album.data:
                item.games.extend(imgur(album.id))
    for x in item.games:
        print("* {}".format(x))
    print()