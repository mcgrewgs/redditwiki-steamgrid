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
    response = requests.get(
        "https://api.imgur.com/3/album/{}".format(
            album),headers=headers)
    response.raise_for_status()
    for x in filter(lambda x:x.startswith("X"),response.headers):
        print("{0}: {1}".format(x,response.headers[x]))
    time.sleep(0.5)
    return response.json(object_hook=builtinext.AttrDict).data



# Blurred dataset

gamenum=0

with open('blurred.yaml') as f:
    dataset = yaml.load(f)

output = []
for item in dataset:
    output.append("### /u/{}".format(item.name))

    if 'threads' in item:
        ids = map(lambda x:"http://redd.it/"+x,item.threads)
        output.append("Threads: {}  ".format(', '.join(ids)))
    if 'images' in item:
        output.append("Images: http://imgur.com/{}  ".format(','.join(item.images)))

    #games list
    if not 'games' in item:
        item.games = []
    if 'albums' in item:
        output.append("Albums:")
        output.append('')
        for album in item.albums:
            ialbum=imgur(album.id)
            print(album.id)
            output.append("* [{0.title} ({0.images_count})]({0.link})".format(ialbum))
            if album.data:
                for image in ialbum.images:
                    item.games.append(
                        "[{0.title}]({0.link})".format(image))

    output.append('')
    output.append('Games:')
    output.append('')
    for x in item.games:
        gamenum+=1
        output.append("* {}".format(x))
    output.append('')
    output.append('- - -')
    output.append('')


output.append('total games: ~{}  \n'.format(gamenum))

open("output.md","w").writelines(str(x)+"\n" for x in output)