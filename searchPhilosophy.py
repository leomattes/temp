import requests
import time
from bs4 import BeautifulSoup

# classes of divs or span used in wiki information or Box
notvalidParentClasses = ['infobox', 'hatnote', 'navigation-not-searchable', 'ambox', 'navbox',
                         'vertical-navbox', 'IPA', 'mw-redirectedfrom', 'hatnote', 'tright',
                         'humbinner', 'noprint', 'reference', 'navbox-title', 'vertical-navbox', 'navbox-vertical']
stopClasses = ['bodyContent']

NotvalidlinkClasses = ('image', 'mw-jump-link', 'mw-jump-link', 'internal')

debug = 0


def getClass( h):
    if 'class' in h.attrs:
        linkclass = h.attrs['class']
        if isinstance(linkclass, str):
            return linkclass
        else:
            str1 = ' '.join(str(e) for e in linkclass)
            return str1
            #return linkclass[0]
    return None

def getClasses( h):
    if 'class' in h.attrs:
        linkclass = h.attrs['class']
        return linkclass
    return None


def isInClass( h, invalids):
    linkclasses = getClasses(h)
    if (linkclasses == None):
        return 0

    for linkclass in linkclasses:
        if linkclass in invalids:
            return 1
    return 0;


def isValidClass( h, invalids):
    linkclasses = getClasses(h)
    if (linkclasses == None):
        return 1

    for linkclass in linkclasses:
        if linkclass in invalids:
            return 0
    return 1;

def isValidid( h, invalids):
    linkclasses =  h.getId()
    if (linkclasses == None):
        return 1

    for linkclass in linkclasses:
        if linkclass in invalids:
            return 0
    return 1;


def isValidClassRecursive( h, invalids):
    if isValidClass(h,  invalids) ==0:
        return 0 # invalid class

    if isValidClass(h,  stopClasses) ==0:
        return 1 # stop

    tag = h.parent
    if tag == None:
        return 1 # stop

    return isValidClassRecursive(tag, invalids);

def isPhilosophy(url):
    if url.find('/wiki/Philosophy') == 0 or url.find('https://en.wikipedia.org/wiki/Philosophy') == 0 :
        return 1
    else:
        return 0

    return 0;



def isValidLink(tag, debug):
    if isValidClass(tag, NotvalidlinkClasses) == 0:
        if debug ==2:
            print("invalid link class")
        return 0

    if isValidClassRecursive(tag, notvalidParentClasses) == 0:
        if debug == 2:
            print("invalid parent class")
        return 0

    if (tag.name =='a')  and  'href' in tag.attrs:
        ref = tag.attrs['href']

        if ref.find('/wiki/File:') == 0:
            return 0
        elif ref.find('/wiki/Help:') == 0:
            return 0
        if ref.find('/wiki/') ==0 :
               return 1

    return 0




def getNextArticle(url, debug):
    if url.find('https') != 0:
        url = 'https://en.wikipedia.org' + url

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    philosophy = isPhilosophy(url);
    if (philosophy ==1):
        return None, philosophy

    main_mody = soup.find(id='bodyContent')
    links = main_mody.find_all('a')

    for h in links:
        if (debug ==2):
            print(h)
        if isValidLink(h, debug)==1  :
           ref = h.attrs['href']
           return ref, philosophy


    return None, philosophy



def LedTosPhilosophy(url, db):
    debug = db
    import time
    urls = []

    philosophy = 0
    while url != None and url not in urls and philosophy == 0:
        if debug > 0:
            print("->>" + url)
        urls.append(url)
        url, philosophy = getNextArticle(url, debug)
        time.sleep(0.5)


    if philosophy == 1:
        print("The article lead to the article Philosophy in " +  str(len(urls)) + " steps .")
        return 1, urls
    elif url in urls:
        print("The article lead to a loop  in " +  str(len(urls)) + " steps .")
    elif url == None:
        print("The Last article there hasn't a valid Link in " +  str(len(urls)) + " steps .")
    return 0, urls



def testRandomic():
    url = "https://en.wikipedia.org/wiki/Special:Random"
    for i in range(0,10):
        isphilosophy, ursl =  LedTosPhilosophy(url, 1)
        if isphilosophy==1 :
            print("     " + str(i) + ' '+ ursl[1] )
        else:
             print("     " +  str(i) + ' ' + ursl[1] )

    print("   fim   " )

def debugurl(url):
    isphilosophy, ursl = LedTosPhilosophy(url, 1)

#testRandomic()
#debugurl('https://en.wikipedia.org/wiki/India')



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('inform the url for the test  ')
    else:
        if sys.argv[1].find('test') == 0:
            print('Testing  randomic ')
            testRandomic()
        else:
            print( 'Testing ', sys.argv[1])
            LedTosPhilosophy(sys.argv[1], 1)


#for url in urls:
 #   print(url,  " -- > ")









