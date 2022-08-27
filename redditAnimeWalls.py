import requests
import shutil
from PIL import Image
import glob
import re


def getNewImages():
    CLIENT_ID = "get from reddit"
    CLIENT_SECRET = "get from reddit"
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    data = {'grant_type': 'password',
            'username': 'Enter your username',
            'password': 'Enter your password'}

    headers = {'User-Agent': 'wallpaperBot'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    params = {'limit': 100}
    # This subs name needs to change to mobile anime wallpapers
    res = requests.get('https://oauth.reddit.com/r/Animewallpaper/top/?t=week',
                       headers=headers, params=params).json()

    postList = res["data"]["children"]

    for post in postList:
        try:
            print(post["data"]["url_overridden_by_dest"])
            pic = requests.get(
                post["data"]["url_overridden_by_dest"], stream=True)
            if pic.status_code == 200:
                # need to figure out a way to identify between png and jpeg
                # galleries causing issues as well
                # also need to filter to folders

                # Can't just use title duplicates are common
                with open(remove_emojis(post["data"]["title"]) + " " + post["data"]["name"]+".png", 'wb') as f:
                    shutil.copyfileobj(pic.raw, f)
                print('Image sucessfully Downloaded: ', post["data"]["title"])
            else:
                print('Image Couldn\'t be retrieved')
        except:
            print('Image Couldn\'t be retrieved')


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def filterImages():
    picsArr = glob.glob('./*.png')
    for image in picsArr:
        try:
            im = Image.open(image)
            width, height = im.size
            print(image + str(width) + " x " + str(height))
            if width < height:
                shutil.move(image, "./mobile/" + image.strip("./"))
            elif height < width:
                shutil.move(image, "./desktop/" + image.strip("./"))
            else:
                print("block")
        except:
            print("failed to move")


if __name__ == '__main__':
    getNewImages()
    filterImages()
