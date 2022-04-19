from fwebUtils import URL, LIST
from fwebCore import HttpRequest, Soup
from fwebCore.Extractor import Extractor
from fwebUtils.LOGGER import Log
import json
import sys

Log = Log("FWEB.Downloader.ArchiveDownloader_v1")

class DownloadWebPage:
    response = None
    status = False
    result = False
    soup = None
    client = False
    # ->
    url = ""
    base_url = ""
    json = {}

    def __init__(self, url):
        sys.setrecursionlimit(5000)
        self.result = True
        self.url = url
        self.base_url = URL.extract_base_url(url)

    @classmethod
    def start_url(cls, url, client="False"):
        newExtractor = cls(url)
        newExtractor.url = url
        newExtractor.client = client
        newExtractor.request()
        if newExtractor.response:
            newExtractor.to_html()
            newExtractor.extract_data()
            print(json.dumps(newExtractor.json, indent=4, default=str))
            return newExtractor
        else:
            Log.i("Request was rejected by Server.")
            return False

    @classmethod
    def start_response(cls, url, response, client="False"):
        if not response:
            return False
        newExtractor = cls(url)
        newExtractor.response = response
        newExtractor.client = client
        newExtractor.to_html()
        newExtractor.extract_data()
        print(json.dumps(newExtractor.json, indent=4, default=str))
        return newExtractor

    def start_soup(self, soup):
        if not soup:
            Log.e("Soup is Empty or None.")
        self.soup = soup
        self.extract_data()
        # self.to_json()
        print(json.dumps(self.json, indent=4, default=str))

    # -> Step One -> Call URL and get Raw HTML back in Response Object.
    def request(self):
        Log.i(f"Making Request to URL = [ {self.url} ]")
        resp = HttpRequest.get_request(self.url)
        if resp:
            self.response = LIST.get(1, resp)

    # -> Step Two -> Convert Response Object to HTML Object
    def to_html(self):
        Log.i(f"Parsing Response Text to HTML Objects.")
        self.soup = Soup.Parse(self.response)

    # -> Step Four -> Extract Data from Elements/Tags
    def extract_data(self):
        Log.i(f"Attempting to Extract Data from HTML Elements.")
        if not self.soup:
            return False
        temp = Extractor.Extract(self.soup, self.url, client=self.client)
        self.json = temp.data
        self.set_json("url", self.url)
        source = URL.get_site_name(self.url)
        self.set_json("client", self.client)
        self.set_json("source", source)
        self.set_json("source_url", f"www.{source}.com")

    def set_json(self, key, value):
        self.json[key] = value

    def check_process(self):
        if not self.response:
            self.result = False
            return False
        if not self.soup:
            self.result = False
            return False
        return True

# if __name__ == '__main__':
#     newTest = "https://towardsdatascience.com/how-to-use-qgis-spatial-algorithms-with-python-scripts-4bf980e39898"  # denied
#     newTest1 = "https://www.cnn.com/2022/03/27/politics/joe-biden-vladimir-putin-ukraine-war/index.html"  # denied
#     newTest2 = "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41"
# #     newTest3 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments"
#     download = "https://www.medium.com"
#     d = DownloadWebPage.start_url(url=download)

