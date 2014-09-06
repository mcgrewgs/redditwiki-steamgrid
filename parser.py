import json,yaml,builtinext,praw,requests,time,warnings

warnings.filterwarnings("ignore")

with open('.auth.json') as f:
    auth = json.load(f,object_hook=builtinext.AttrDict)


yaml.add_constructor(
    u'tag:yaml.org,2002:map',
    lambda loader,node:builtinext.AttrDict(loader.construct_mapping(node))
)


#listgrabber
def imgur(album):
    time.sleep(0.5)
    print('- - - - - - - - - - - -')
    print(album)
    headers = auth.imgur
    response = requests.get(
        "https://api.imgur.com/3/album/{}".format(
            album),headers=headers)

    for x in filter(
            lambda x:x.startswith("X-Rate") and
                     x.endswith('Remaining'),
            response.headers
      ):
        print("{0}: {1}".format(x,response.headers[x]))

    response.raise_for_status()
    return response.json(object_hook=builtinext.AttrDict).data



# Blurred dataset


with open('blurred.yaml') as f:
    dataset = yaml.load(f)

output = []
gamenum=0
imagenum=0
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
            imagenum += ialbum.images_count
            output.append("* [{0.title} ({0.images_count}){1}]({0.link})".format(ialbum, " (Automated)" if album.data else ""))
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


output.append('total games: ~{}  '.format(gamenum))
output.append('total images: ~{}  \n'.format(imagenum))

open("output.md","w").writelines(str(x)+"\n" for x in output)