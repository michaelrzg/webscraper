# Michael Rizig
# CS7263
# Professor Jiho Noh
# 6/2/25
# WebCrawler

from urllib.request import HTTPError, urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
class Crawler:
    def __init__(self, seed):
        self.queue = []
        self.queue.append(seed)
        self.seed = seed
        self.library = {}
        self.counter = 0

    #check if link is ok to proceed with (based on the rules in the assignment)
    def is_url_ok_to_follow(self,url):
        if not isinstance(url,str):
            return False
        if url in self.library:
            return False
        remove_anchor = url.split("#")[0]
        remove_queries = remove_anchor.split("?")[0]
        parts = remove_queries.split("/")

        if parts[0]!= 'https:' and parts[0] != "http:":
            return False
        if parts[2]!= 'nlp.stanford.edu':
            return False
        if '.html' not in parts[-1] and '.html' not in parts[-1]:
            return False

        return True

    # get the raw html code in the correct encoding format
    def get_html(self,url):
        #print(url)
        try:
            page = urlopen(url)
            encoding = page.info().get_content_charset()
            html = page.read().decode(encoding)
            return html
        except Exception as e:
            print(e)

    # discover all links on page
    def discover_urls(self,soup,pageurl):
        # get links
        for link in soup.find_all('a'):
            link = self.check_relative_link(link.get("href"),pageurl)
            if self.is_url_ok_to_follow(link):
                self.queue.append(self.clean_url(link))

    # check if linkn is relative and if it is convert it to full link
    def check_relative_link(self,url,pageurl):
        if isinstance(url,str):

            if len(url.split("/"))==1:
                return urljoin(pageurl,url)
            return url
    # remove the anchor and queries from link
    def clean_url(self,url):
        remove_anchor = url.split("#")[0]
        remove_queries = remove_anchor.split("?")[0]
        return remove_queries

    # get the title and info of link
    def extract_info(self,url,soup):
        url = self.clean_url(url)
        self.library[url] = (soup.title.string, soup.get_text())

    def save_webpages(self,library):
        index=0
        for key in library:
            with open(f"webpages/{index}-{library[key][0].replace("/","").replace(".","")}.txt",'w') as file:
                file.write(""+library[key][1])
                file.flush()
                index+=1

    # run
    def crawl(self):
        while(len(self.queue)!=0):
            nextlink = self.queue.pop()
            # first check if link is ok
            if not self.is_url_ok_to_follow(nextlink):
                continue
            # get html data and decode
            html = self.get_html(nextlink)
            # create soup object for functions to use
            if html==None:
                continue
            soup = BeautifulSoup(html,"html.parser")
            # get title and text
            self.extract_info(nextlink,soup)
            # discover new links and add them to the queeu
            self.discover_urls(soup,nextlink)
            self.counter+=1
        self.save_webpages(self.library)


crawler = Crawler("https://nlp.stanford.edu/IR-book/information-retrieval-book.html")
crawler.crawl()
