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
    return list(response.json(object_hook=builtinext.AttrDict).data.images)



# Blurred dataset

gamenum=0

with open('blurred.yaml') as f:
    dataset = yaml.load(f)

output = []
for item in dataset:
    output.append("### /u/{}".format(item.name))
    if 'albums' in item:
        ids = map(lambda x:"http://imgur.com/a/"+x.id,item.albums)
        output.append("Albums: {}  ".format(', '.join(ids)))
    if 'threads' in item:
        ids = map(lambda x:"http://redd.it/"+x,item.threads)
        output.append("Threads: {}  ".format(', '.join(ids)))
    if 'images' in item:
        output.append("Images: http://imgur.com/{}  ".format(','.join(item.images)))
    
    output.append('')

    #games list
    if not 'games' in item:
        item.games = []
    if 'albums' in item:
        for album in item.albums:
            if album.data:
                for image in imgur(album.id):
                    item.games.append("[{0.title}]({0.link})".format(image))
    for x in item.games:
        gamenum+=1
        output.append("* {}".format(x))
    output.append('')
output.append('- - -')
output.append('total games: ~{}  \n'.format(gamenum))

open("output.md","w").writelines(str(x)+"\n" for x in output)