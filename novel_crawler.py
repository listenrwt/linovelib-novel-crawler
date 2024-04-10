import requests, parsel, time, os, re

no_of_books = 3944
delayTime = 0.5
maxFailTime = 3
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

def removeInvalid(text: str):
    return text.replace('/', '_').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('\"', '').replace('<', '').replace('>', '').replace('|', '').replace('\'', '')

def grapTextFromContentURL(url, series_title, failTime = 0):

    response = requests.get(url, headers=header)
    content = response.text.replace('<br>', '<p>\n</p>')

    if(response.status_code != 200):
        if(failTime < maxFailTime):
            print(('url: ' + str(url) +' series_title: ' + str(series_title) + ' code: ' + str(response.status_code) + '\n'))
            time.sleep(delayTime)
            grapTextFromContentURL(url, series_title, failTime + 1)
        else:
            with open('errorLog.txt', mode='a', encoding='utf-8') as f:
                f.write('url: ' + str(url) +' series_title: ' + str(series_title) + ' code: ' + str(response.status_code) + '\n')
            return 'None'

    selector = parsel.Selector(content)

    next_url = ""
    try:
        next_url = selector.css('link[rel="prerender"]').attrib['href']
    except KeyError:
        return 'None'

    book_title = selector.css('.atitle h3::text').get()
    chapter = selector.css('.atitle h1::text').get()
    content_list = selector.css('.acontent p::text').getall()
    if (book_title is None) or (chapter is None) or (content_list is None):
        return 'None'
    content = '\n'.join(content_list)

    if len(content_list) > 0:
        print(series_title + ' ' + book_title + ':' + chapter + ' is loaded.')
        book_title = removeInvalid(str(book_title))
        chapter = removeInvalid(str(chapter))
        chapter = re.sub(r"（[^（）]*）", "", chapter)

        file_path = os.path.join(series_title, book_title, chapter + ".txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(content)
    else:
        print(series_title + ' ' + book_title + ':' + chapter + ' has no content(manga or pictures).')

    time.sleep(delayTime)
    return next_url
    #grapTextFromContentURL(next_url, series_title)

def grapBookFromCatalogURL(catalog_url, failTime = 0):
    response = requests.get(catalog_url, headers=header)

    if(response.status_code != 200):
        if(failTime < maxFailTime):
            print('url: ' + str(catalog_url) + ' code: ' + str(response.status_code) + '\n')
            time.sleep(delayTime)
            grapBookFromCatalogURL(catalog_url, failTime + 1)
        else:
            with open('errorLog.txt', mode='a', encoding='utf-8') as f:
                f.write('url: ' + str(catalog_url) + ' code: ' + str(response.status_code) + '\n')
            return

    selector = parsel.Selector(response.text)

    firstPage_url = selector.css('a.chapter-li-a::attr(href)').get()

    series_title = selector.css('a.btn-blank::text').get()
    if(series_title is None):
        series_title = selector.css('h1.btn-blank::text').get()
    series_title = removeInvalid(str(series_title))

    time.sleep(delayTime)
    currenturl = 'https://tw.linovelib.com/' + firstPage_url
    while True:
        currenturl = grapTextFromContentURL(currenturl, series_title)
        if(currenturl == 'None'):
            break
    
def midProcessing(midURL, series_title):
    currenturl = midURL
    while True:
        currenturl = grapTextFromContentURL(currenturl, series_title)
        if(currenturl == 'None'):
            break


for i in range(1, no_of_books + 1):
    try:    
        grapBookFromCatalogURL("https://tw.linovelib.com/novel/" + str(i) + "/catalog")
        with open('progressLog.txt', mode='w', encoding='utf-8') as f:
            f.write('finished: ' + str(i) + " continue: " + str(i + 1))
    except Exception as e:
        with open('errorLog.txt', mode='a', encoding='utf-8') as f:
            f.write('number: ' + str(i) + ' with exception ' + str(e) + '\n')
        continue
