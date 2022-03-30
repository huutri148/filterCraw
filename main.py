import os
import requests
import hashlib
import hmac
import json
import time
import datetime
import string
from threading import Thread
from pathlib import Path





#########################################################
ID = "ZOZ0WD80"
CTIME = "1648572551"
INFO_PATH = "/api/v2/song/get/info"
STREAM_PATH = "/api/v2/song/get/streaming"
LYRIC_PATH = "/api/v2/lyric/get/lyric"
PLAYLIST_PATH = "/api/v2/page/get/playlist"
SECRET_KEY ="2aa2d1c561e809b267f3638c4a307aab"
API_KEY = "88265e23d4284f25963e6eedac8fbfa3"
PAGE = "https://zingmp3.vn"
COOKIE = "_ga=GA1.2.1689943077.1633748883; zpsid=eMqpTcwdFagwSovBAunT1hi0MbKiZrK2lHjJJrtlFLwk76fvMCS1MQypHNGqv0batYn1AasXD1shBreHFiyAGCX7UKO7nIz6o0z4GolPGqwm0XXfL65J; zmp3_sid=c_gzNVP3H665_RvLyaLVQ9-CtZskLbXHgOds0QbNTtwavTK9b2PeUlgSa3JjKsjXmU_-2h0m0qAMrlGljZ1BVvFww4E-I4OZkPVeTTHcIW2ailPiP0; __zi=3000.SSZzejyD0jSbZUgxWaGPoJIFlgNCIW6AQ9sqkju84vn_sElysGbNq7ZRu_ZVG5VIU9Jb-jHAMTGmCZK.1; __zi-legacy=3000.SSZzejyD0jSbZUgxWaGPoJIFlgNCIW6AQ9sqkju84vn_sElysGbNq7ZRu_ZVG5VIU9Jb-jHAMTGmCZK.1; _gid=GA1.2.57731014.1648537576; _zlang=vn; adtimaUserId=3000.SSZzejyD0jSbZUgxWaGPoJIFlgNCIW6AQ9sqkju84vn_sElysGbNq7ZRu_ZVG5VIU9Jb-jHAMTGmCZK.1; zmp3_app_version.1=1611; _gat=1; atmpv=1; zmp3_rqid=MHwxMTMdUngMTYxLjmUsIC3LjgyfHYxLjYdUngMTF8MTY0ODY0NDYzNzk0Mw"


# Genres, artist, albums dictionary
GENRES = []
ARTISTS = []
TYPES = []
ALBUMS = []
ALBUM ={}
#######################################################
def Hash256(value):
    h = hashlib.sha256(value.encode('utf-8'))
    return h.hexdigest()

def Hash512(value, key):
    return hmac.new(key.encode('utf-8'), value.encode('utf-8'), hashlib.sha512).hexdigest()

def getSongUrl(id, ctime):
    sig = Hash512(INFO_PATH + Hash256("ctime=" + ctime + "id=" + id + "version=1.6"),
                  SECRET_KEY)
    return PAGE + INFO_PATH + "?id=" + id + "&ctime=" + ctime + "&version=1.6&sig="+ sig + "&apiKey=" + API_KEY

def getLyricUrl(id, ctime):
    sig = Hash512(LYRIC_PATH+ Hash256("ctime=" + ctime + "id=" + id + "version=1.6"),
                  SECRET_KEY)
    return PAGE + LYRIC_PATH+ "?id=" + id + "&BGId=0&ctime=" + ctime + "&version=1.6&sig="+ sig + "&apiKey=" + API_KEY

def getStreamUrl(id, ctime):
    sig = Hash512(STREAM_PATH+ Hash256("ctime=" + ctime + "id=" + id + "version=1.6"),
                  SECRET_KEY)
    return PAGE + STREAM_PATH+ "?id=" + id + "&ctime=" + ctime + "&version=1.6&sig="+ sig + "&apiKey=" + API_KEY

def getPlaylistUrl(id, ctime):
    sig = Hash512(PLAYLIST_PATH+ Hash256("ctime=" + ctime + "id=" + id + "version=1.6"),
                  SECRET_KEY)
    return PAGE + PLAYLIST_PATH+ "?id=" + id + "&ctime=" + ctime + "&version=1.6&sig="+ sig + "&apiKey=" + API_KEY
#################################################
def WriteData(path, data):
    f = open(path, 'a+', encoding='utf-8')
    obj = json.dumps(data, ensure_ascii=False).encode('utf8')
    f.write(obj.decode()+"\n")

def WriteSong(path, data):
    f = open(path, 'a+', encoding='utf-8')
    obj = json.dumps(data, ensure_ascii=False).encode('utf8')
    f.write(obj.decode()+"\n")

def WriteError(path, data):
    f = open(path,'a+', encoding='utf-8')
    obj = json.dumps(data, ensure_ascii=False).encode('utf8')
    f.write(obj.decode() + "\n")

def WriteTotal():
    global GENRES
    global ARTISTS
    global TYPES

    streamFiles = next(os.walk("./Data/streaming"))[2]
    lyricFiles = next(os.walk("./Data/lyric"))[2]
    beatFiles = next(os.walk("./Data/beat"))[2]
    inforFiles = next(os.walk("./Data/song"))[2]

    f = open("./total.txt", 'a+', encoding='utf-8')

    f.write("Stream Files: {} files\n".format(len(streamFiles)))
    f.write("Lyric Files: {} files\n".format(len(lyricFiles)))
    f.write("Beat Files: {} files\n".format(len(beatFiles)))
    f.write("Genres: {} types\n".format(len(GENRES)))
    f.write("Classes: {} types\n".format(len(TYPES)))
    f.write("Artists: {}\n".format(len(ARTISTS)))

####################################################
def ResolveAlbum(obj):

    # current Album
    global ALBUM
    global ALBUMS
    ALBUM = obj['encodeId']

    albumObj = {"id": obj['encodeId'], "title":obj['title'], "thumbnail": obj['thumbnail'],
                "releaseDate": obj['releaseDate'], "sortDescription":obj['sortDescription'],
                "artistsNames":obj['artistsNames'], "like":obj['like'], "listen":obj['listen']}
    albumPath = "./Data/album/" + obj['encodeId']+ "/"

    if len(ALBUMS) == 0:
        ALBUMS.append(obj['encodeId'])
        if not os.path.isdir(albumPath):
            os.makedirs(albumPath)
        WriteData(albumPath + "info.txt", albumObj)
    elif obj['encodeId'] not in ALBUMS:
        ALBUMS.append(obj['encodeId'])
        if not os.path.isdir(albumPath):
            os.makedirs(albumPath)
        WriteData(albumPath+ "info.txt", albumObj)

def ResolveInfoObj(obj):
    global ALBUM
    global ALBUMS
    global GENRES
    global ARTISTS
    global TYPES

    # reduce redundant prop
    if "isOffical" in obj:
        del obj['isOffical']
    if "username" in obj:
        del obj['username']
    if "comment" in obj:
        del obj['comment']
    if "isWorldWide" in obj:
        del obj['isWorldWide']
    if "isZMA" in obj:
        del obj['isZMA']
    if "zingChoise" in obj:
        del obj['zingChoise']
    if "isPrivate" in obj:
        del obj['isPrivate']
    if "preRelease" in obj:
        del obj['preRelease']
    if "radioId" in obj:
        del obj['radioId']
    if "streamingStatus" in obj:
        del obj['streamingStatus']
    if "album" in obj:
        del obj['album']
    if "allowAudioAds" in obj:
        del obj['allowAudioAds']
    if "userid" in obj:
        del obj['userid']
    if "radio" in obj:
        del obj['radio']
    if "isRBT" in obj:
        del obj['isRBT']
    if "listen" in obj:
        del obj['listen']
    if "liked" in obj:
        del obj['liked']

    # Song Obj to write to Album, Genre, Type
    writedObj = {'encodeId': obj['encodeId'],'title': obj['title']}

    # Write Artist Data
    listArt = []
    if 'artists' in obj:
        for art in obj['artists']:
            listArt.append({'id': art['id'], 'name':art['name']})
            artPath = "./Data/art/" + art['id'] + "/"
            artObj = {'id': art['id'], 'name':art['name'], 'alias': art['alias'],
                      'thumbnail': art['thumbnail'], 'thumbnailM': art['thumbnailM']}
            if len(ARTISTS) == 0:
                ARTISTS.append(art['id'])
                if not os.path.isdir(artPath):
                    os.makedirs(artPath)
                WriteData(artPath + "info.txt", artObj)
            elif art['id'] not in ARTISTS:
                ARTISTS.append(art['id'])
                if not os.path.isdir(artPath):
                    os.makedirs(artPath)
                WriteData(artPath + "info.txt", artObj)
            WriteData(artPath + "songs.txt", writedObj)
    obj['artists'] = listArt


    # Write Genres Data
    listGenres = []
    types =""
    if 'genres' in obj:
        for gen in obj['genres']:
            types+=gen['alias']+"-"
            listGenres.append({"id": gen['id'], "name":gen['name']})
            genPath = "./Data/genre.txt"
            genreFile = "./Data/genre/" + gen['id'] + ".txt"
            genObj = {"id": gen['id'], "name":gen['name']}
            if len(GENRES) == 0:
                GENRES.append(gen['id'])
                WriteData(genPath, genObj)
            elif gen['id'] not in GENRES:
                GENRES.append(gen['id'])
                WriteData(genPath, genObj)
            WriteData(genreFile, writedObj)
    obj["genres"] =listGenres

    # Write Type Data for classification
    obj["types"]= types
    typeFile = "./Data/type.txt"
    typePath = "./Data/type/" + types + ".txt"
    if len(TYPES) == 0:
        TYPES.append(types)
        typeObj = {"id": (len(TYPES) - 1), "title":types}
        WriteData(typeFile, typeObj)
    elif types not in TYPES:
        TYPES.append(types)
        typeObj = {"id": (len(TYPES) - 1), "title":types}
        WriteData(typeFile, typeObj)
    WriteData(typePath, writedObj)

    # Add track for album
    albumPath = "./Data/album/"  + ALBUM + "/songs.txt"
    WriteData(albumPath, writedObj)

    return obj


def ResolveStreamObj(url,Id):
    res = requests.get(url)
    with open("./Data/streaming/" + Id + ".mp3",  "wb") as f:
        f.write(res.content)

def ResolveLyricObj(data,Id):

    # File kara
    if "sentences" in data:
        myFile = Path('./Data/lyric/'+ Id + ".txt")
        if not(myFile.is_file()):
            sen = data['sentences']
            obj = json.dumps(sen, ensure_ascii=False).encode('utf8')

            with open("./Data/lyric/" + Id + ".txt",  "wb") as f:
                f.write(obj)

    #File lyric
    if "file" in data:
        myFile = Path('./Data/lyric/'+ Id + ".lrc")
        if not(myFile.is_file()):
            lrcFile = requests.get(data['file'],timeout=10)
            with open("./Data/lyric/"+ Id + ".lrc", "wb") as f:
                f.write(lrcFile.content)

    #File Beat
    if "beat" in data:
        print(data['beat'])
        beatFile = requests.get(data['beat'], timeout=10)
        with open("./Data/beat/" + Id + ".m4a","wb") as f:
            f.write(beatFile.content)

def ReadCookie(path):
    f = open(path,)
    data = json.load(f)
    global COOKIE
    COOKIE = data['cookies']




####################################################################
# Download file MP3
def process_Streaming(id, cook):
    print("Streaming: " + id)
    try:
        url = getStreamUrl(id, CTIME)
        res = requests.get(url,headers={"cookie":cook})
        obj = res.json()
        try:
            if obj['err'] == -201:
                print("\nCOOKIE Expired")
                global COOKIE
                cok = res.headers["Set-Cookie"]
                COOKIE = cook
                return process_Streaming( id, COOKIE)
            elif obj['err']== -1023:
                return id
            elif obj['err'] == -112:
                print('Private Data')
            elif obj['err'] == -1150:
                print('Vip Role Resquest:' + id)
            elif obj['err'] == 0:
                data = obj['data']
                ResolveStreamObj(data['128'], id)
            else:
                print("Some error occur")
                WriteError("error.txt", obj)
        except:
            print("Some thing else occur")
        finally:
            return id
    except:
        print("Error")
    return id


# Save info of the song
def process_Info(id, cook):
    print("Info: " + id)
    try:
        url = getSongUrl(id, CTIME)
        res = requests.get(url,headers={"cookie":cook})
        obj = res.json()
        try:

            if obj['err'] == -201:
                print("\nCOOKIE Expired")
                global COOKIE
                cok = res.headers["Set-Cookie"]
                COOKIE = cook
                return process_Info(id, COOKIE)
            elif obj['err']== -1023:
                return id
            elif obj['err'] == -112:
                print('Private Data')
            elif obj['err'] == 0:
                myFile = Path('./Data/song/'+ id+ ".txt")
                if not(myFile.is_file()):
                    rObj = ResolveInfoObj(obj['data'])
                    WriteData("./Data/song/" + rObj['encodeId'] +".txt", rObj)
            else:
                print("Some error occur")
                WriteError("error.txt", obj)
        except:
            print("Some thing else occur")
        finally:
            return id
    except:
        print("Error")
    return id


# Save Lyrics, Kara, Beat of the song
def process_Lyric(id, cook):
    print("Lyric: " + id )
    try:
        url = getLyricUrl(id, CTIME)
        res = requests.get(url,headers={"cookie":cook})
        obj = res.json()
        try:
            if obj['err'] == -201:
                print("\nCOOKIE Expired")
                global COOKIE
                cok = res.headers["Set-Cookie"]
                COOKIE = cok
                return process_Lyric(id, COOKIE)
            elif obj['err']== -1023:
                return id
            elif obj['err'] == -112:
                print('Private Data')
            elif obj['err'] == 0:
                ResolveLyricObj(obj['data'],id)
            else:
                print("Some error occur")
                WriteError("error.txt", obj)
        except:
            print("There is no lyric for this song: " + id)
        finally:
            return id
    except:
        print("Error")
    return id


def threaded_process_range(nthreads, id):
    storeStreaming = {}
    threadsStreaming= []
    storeLyric = {}
    threadsLyric = []
    storeInfo = {}
    threadsInfo = []

    t1 = Thread(target = process_Streaming , args=(id, COOKIE))
    t2 = Thread(target =process_Lyric, args=(id, COOKIE))
    t3 = Thread(target = process_Info, args=(id, COOKIE))

    threadsStreaming.append(t1)
    threadsLyric.append(t2)
    threadsInfo.append(t3)



    #start the threads
    [ t1.start() for t1 in threadsStreaming]
    [ t2.start() for t2 in threadsLyric]
    [ t3.start() for t3 in threadsInfo]
    #wait for the theads to finish
    [t1.join() for t1 in threadsStreaming]
    [t2.join() for t2 in threadsLyric]
    [t3.join() for t3 in threadsInfo]


    return storeLyric.update(storeStreaming)


def AnalysePlaylist(playlistID,cook):
    url = getPlaylistUrl(playlistID,CTIME);
    res = requests.get(url, headers={"cookie":cook},timeout = 10)
    obj = res.json()
    try:
        if obj['err'] == -201:
            print("\nCOOKIE expired")
            global COOKIE
            cok = res.headers["Set-Cookie"]
            COOKIE = cook
            return AnalysePlaylist(playlistID)
        elif obj['err'] == -1023:
            print("\nPlaylist not found: " + playlistID)
            return playlistID
        elif obj['err'] == 0:
            data = obj['data']
            ResolveAlbum(data)
            songs = data['song']
            for song in songs['items']:
                    threaded_process_range(1, song['encodeId'])
    except:
        print("PL Something else occur: " + playlistID )
    finally:
        return playlistID

def Clone():
    playlistID = "ZOUBOE9F";
    AnalysePlaylist(playlistID,COOKIE)
    playListFile = open('Playlist.txt', 'r')
    Lines = playListFile.readlines()

    for line in Lines:
        print("\nPlaylist ID: " + line.strip())
        AnalysePlaylist(line.strip(),COOKIE)
    WriteTotal()
if  __name__ == '__main__':
   Clone()
