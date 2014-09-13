import requests                                         #HTTP library
from bs4 import BeautifulSoup                           #HTML parser library
import sys
import re                                               #regex library

path = "C:\\temp\\"                                     #define new path for pictures, must make dir ahead of time
sys.path.insert(0, path)                                #use new path in working directories

i = 1                                                   #starting subdomain integer

r = requests.get("http://xkcd.com/")

namePat = "http:\/\/imgs\.xkcd\.com\/comics\/(\w+)"     #used later, finds image name in url

while r.status_code == 200:

    r = requests.get("http://xkcd.com/%d" % i)          #get url HTTP at specific subdomain number

    soup = BeautifulSoup(r.text)                        #parses request content text and keeps only HTML

    comic = str(soup.find(id = "comic"))                #finds the "comic" div within the HTML that holds the url, convert to string for regex

    imageLink = re.findall('src="(.*?[^\"])"', comic)   #searches for and keeps anything inside the img src tag and discards the quotation marks

    try:
        getImage = requests.get(imageLink[0])           #get found image HTTP and name, imageLink and name return lists, access actual link by [0]
        name = re.findall(namePat, imageLink[0])
    except IndexError:
        i+=1                                            #if no image, continue to next iteration
        continue

    ifJPEG = re.findall("\.jpg", imageLink[0])          #will return a list of one element if .jpg extension is found

    ifGIF = re.findall("\.gif", imageLink[0])           #will return a list of one element if .gif extension is found

    if len(ifJPEG) == 1:
        newPath = "%s%d%s" % (path, i, ".jpg")          #if jpg found, save as jpg
        
    elif len(ifGIF) == 1:
        newPath = "%s%d%s" % (path, i, ".gif")          #if gif found, save as gif
        
    else:
        newPath = "%s%d%s" % (path, i, ".png")          #png found, png saved

    print "Getting %d: %s" % (i, name[0])               #status message

    with open(newPath, 'wb') as f:                      #open new path for image (created if doesn't exist)
        f.write(getImage.content)                       #write image to path

    i += 1                                              #iterate to new url subdomain for the loop
    if i == 404:                                        #if 404 is next, skip it
        i+=1
