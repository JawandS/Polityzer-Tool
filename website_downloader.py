import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from twisted.internet.error import ConnectionRefusedError
from urllib.parse import urlparse, urljoin
import tldextract
from bs4 import BeautifulSoup as bs
import logging
import time
import os
import csv
import re
import requests


import config, utils

_Logger = logging.getLogger(__name__)


class WebsiteCrawler(scrapy.Spider):
    """Main class handling the download of the websites"""

    name = "website_crawler"
    chromedriver_path = config.CHROMEDRIVER_PATH
    handle_httpstatus_list = [200, 301]
    link_extractor = LinkExtractor()
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_TIMEOUT": 20,
        "SELENIUM_DRIVER_NAME": "chrome",
        "DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800},
        # "SELENIUM_DRIVER_EXECUTABLE_PATH": chromedriver_path,
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def __init__(self) -> None:
        self.website_input_file = config.CANDIDATE_OFFICE_WEBSITE
        self.database_file = utils.get_database_file()
        self.javascript_file = utils.get_javascript_database_file()
        self.error_file = utils.get_error_file()
        self.headers = config.HEADERS
        self.cache = set()

    def loadCampaignSites(self):
        """Load name and websites to be downloaded"""

        results = set()
        if not os.path.isfile(self.website_input_file):
            _Logger.error("No input file detected!")
            return results
        input_file = self.website_input_file

        with open(input_file, "r") as inputfile:
            csvreader = csv.DictReader(inputfile, delimiter=",")
            # next(csvreader)
            for row in csvreader:
                name = row["fec_name"].replace(",", "").replace(" ", "").replace("/", "")  # row[0]
                office = row["office"]  # row[1]
                site = row["website"]  # row[-1]
                if site is None or len(site) == 0:
                    continue
                results.add((name, office, site))
        return results

    def saveHtml(self, response, depth):
        """
        Save the response to a html file.
        Note: Filenames are appended with random integers to avoid duplicates.
        """

        candidate_name = response.meta["name"].replace(" ", "")

        # create office folder
        candidate_office = response.meta["office"]
        office_download_folder = os.path.join(config.HTML_FOLDER, candidate_office)
        if not os.path.isdir(office_download_folder):
            os.mkdir(office_download_folder)

        # create candidate folder
        fullpath = os.path.join(office_download_folder, candidate_name)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)

        # create PDF folder
        pdf_folder = os.path.join(fullpath, "pdfs")
        if not os.path.exists(pdf_folder):
            os.mkdir(pdf_folder)

        try:
            page_title = response.css("title::text").get()
        except Exception as e:
            _Logger.error(f"Error getting page title: {e}. May not be an HTML page.")
            page_title = None

        current_url = response.meta["url"]
        # pdf_flag = False
        if current_url.endswith(".pdf"):
            fullpath = pdf_folder
            # pdf_flag = True

        relativeurlpath = urlparse(current_url).path
        rooturlpath = urlparse(current_url).netloc
        randomizer = str(time.time()).replace(".", "")
        if relativeurlpath:
            relativepath = relativeurlpath.replace("/", "|")
            filetocreate = os.path.join(fullpath, "".join([rooturlpath, relativepath, randomizer]))
        else:
            if page_title:
                filetocreate = os.path.join(fullpath, "".join([rooturlpath, page_title, randomizer]))
            else:
                filetocreate = os.path.join(fullpath, "".join([rooturlpath, randomizer]))

        _Logger.info(f"Saving {response.url}, Path -> {filetocreate}")
        with open(filetocreate, "wb") as f:
            f.write(response.body)
            self.database_file.writerow([candidate_name, current_url, filetocreate, depth])
            self.cache.add(utils.get_hashcode(current_url))
        # utils.attachment_cleaner()

    def saveJavascript(self, response, depth):
        """Extract and save javascript files from the page."""
        soup = bs(response.body, "html.parser")
        candidate_name = response.meta["name"].replace(" ", "")

        # create office folder
        candidate_office = response.meta["office"]
        office_download_folder = os.path.join(config.HTML_FOLDER, candidate_office)
        if not os.path.isdir(office_download_folder):
            os.mkdir(office_download_folder)

        # create candidate folder
        fullpath = os.path.join(office_download_folder, candidate_name)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)

        # creat javascript folder
        javascript_folder = os.path.join(fullpath, "javascript")
        if not os.path.exists(javascript_folder):
            os.mkdir(javascript_folder)

        all_javascript_links_in_page = []
        for script in soup.find_all("script"):
            src = script.get("src")
            if src:
                all_javascript_links_in_page.append(src)

        for link in all_javascript_links_in_page:
            if not link.startswith("https:") and not link.startswith("http:"):
                if link.startswith("//"):
                    link = "https:" + link
                else:
                    link = urljoin(response.meta["url"], link)
            if not link.endswith(".js"):
                link += ".js"

            if utils.get_hashcode(link) in self.cache:
                continue

            javascript_content = requests.get(link, headers=self.headers)

            randomizer = str(time.time()).replace(".", "")
            javascript_filename = link.replace(".js", "").split("/")[-1]
            if len(javascript_filename) > 200:
                _Logger.warning(f"Javascript filename too long: {javascript_filename}. Truncating to 200 characters.")
                javascript_filename = javascript_filename[-200:]

            filetocreate = os.path.join(javascript_folder, javascript_filename + "|" + randomizer + ".js")

            # save the javascript file
            with open(filetocreate, "wb") as f:
                f.write(javascript_content.content)
                self.javascript_file.writerow([candidate_name, link, filetocreate, depth])
                self.cache.add(utils.get_hashcode(link))

    def start_requests(self):
        """Method for the starting of the website requests"""

        _Logger.info("----------download started-----------")

        sites = self.loadCampaignSites()
        for name, office, link in sites:
            self.cache = set()
            _Logger.info(f"Working on {name}->{office}->{link}")

            # this check is to let the same url pass through for wixsites, which require the full url with extra path, whereas for other sites, we want to start from the root domain ideally
            parsed_link = tldextract.extract(link).domain
            if parsed_link.strip().lower() != "wixsite":
                parsed_link = urlparse(link)
                if parsed_link.scheme:
                    link = parsed_link.scheme + "://" + parsed_link.netloc
                else:
                    link = "https://" + parsed_link.netloc

            if link.startswith("file://"):
                yield scrapy.Request(
                    url=link,
                    callback=self.crawlCampaignSite,
                    errback=self.error_handler,
                    meta={"name": name, "office": office, "url": link, "depth": 0},
                    headers=self.headers,
                )
            else:
                yield SeleniumRequest(
                    url=link,
                    callback=self.crawlCampaignSite,
                    errback=self.error_handler,
                    meta={"name": name, "office": office, "url": link, "depth": 0},
                    headers=self.headers,
                )

    def crawlCampaignSite(self, response):
        """Callback method that handles the subsequent webpage downloads once the process begins with 'start_requests' methods"""

        depth = response.meta["depth"]
        _Logger.debug(f"{str(response.url)}, {str(response.status)}, {str(response.meta['url'])}")

        if str(response.status) != "200":
            _Logger.error(str(response.status) + " error on url " + str(response.url) + "\n")

        # save the current link
        self.saveHtml(response, depth=depth)
        self.saveJavascript(response, depth=depth)

        if response.meta["depth"] > config.MAX_DEPTH:
            return

        if response.meta["url"].endswith(".pdf"):
            return

        foundLink = False
        # links = self.link_extractor.extract_links(response)
        for link in response.xpath("//a"):
            # for link in links:
            foundLink = True
            destLink = link.xpath("@href").extract_first()
            # destLink = link.url
            if destLink is None or len(destLink) == 0 or utils.skipUrl(destLink):
                _Logger.debug(f"{destLink} ignored")
                continue

            if not utils.isSameDomain(response.meta["url"], destLink):
                if not destLink.endswith(".pdf"):
                    _Logger.debug(f"{destLink} ignored. Outbound link.")
                    continue

            if not utils.isAbsolute(destLink):
                destLink = urljoin(response.meta["url"], destLink)

            if not re.search(r"^http(s)?:", destLink):
                _Logger.debug(f"{destLink} ignored. Not proper link")
                continue

            if utils.get_hashcode(destLink) in self.cache:
                continue

            _Logger.debug(f"Found link: {destLink}")

            if destLink.startswith("file://"):
                yield scrapy.Request(
                    url=destLink,
                    callback=self.crawlCampaignSite,
                    errback=self.error_handler,
                    meta={
                        "name": response.meta["name"],
                        "office": response.meta["office"],
                        "url": destLink,
                        "depth": depth + 1,
                    },
                    headers=self.headers,
                )
            else:
                yield SeleniumRequest(
                    url=destLink,
                    callback=self.crawlCampaignSite,
                    errback=self.error_handler,
                    meta={
                        "name": response.meta["name"],
                        "office": response.meta["office"],
                        "url": destLink,
                        "depth": depth + 1,
                    },
                    headers=self.headers,
                )
        if not foundLink:
            _Logger.debug(f"No Links... {response.meta['url']}, {response.url}, {str(response.status)}")

    def error_handler(self, failure):
        """callback method that handles logging of errors as they arise"""

        _Logger.info("Logging error from the error handler")
        _Logger.error(repr(failure))
        response = failure.request
        error_url = response.meta["url"]
        error_candidate = response.meta["name"]
        error_depth = response.meta["depth"]
        if failure.check(ConnectionRefusedError):
            error_msg = "Connection was refused by other side: ConnectionRefusedError"
        else:
            # error_msg = failure.getErrorMessage()
            error_msg = repr(failure)
        self.error_file.writerow([error_candidate, error_url, error_depth, error_msg])


def start():
    # if not utils.configure_ChromeDriver():
    #     _Logger.error("Error setting up selenium..")
    #     return

    # create folder to save webpages
    download_flag = False if utils.get_download_status() else True

    # start crawling process
    if download_flag:
        start_time = time.time()
        process = CrawlerProcess()
        process.crawl(WebsiteCrawler)
        process.start()
        _Logger.info(f"----Time taken in seconds----:{time.time() - start_time}")
    else:
        _Logger.info("Download already completed")


if __name__ == "__main__":
    start()
