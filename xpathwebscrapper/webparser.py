import re
from lxml import html
import requests
from urllib.parse import urlparse, urlunparse, urljoin, parse_qs, urlencode
from collections import namedtuple
from xpathwebscrapper.utils import Config
from xpathwebscrapper.utils import Toolbox as tb

import sys

class XpthPattern:
    def __init__(self):
        self.tree = None
        self.row = ''
        self.data_dict = {}
        self.links = []

    def DataColumns(self):
        return self.XPathDataDict().keys()

    def setRowXpath(self, row: str):
        self.row = row

    def XPathDataDict(self):
        return self.data_dict

    def setXPathDataDict(self, cols: dict):
        self.data_dict = cols

    def setLinks(self, links: list):
        self.links = links


class XpthParser:
    def __init__(self, xppattern: XpthPattern):
        self.tree = None

        self.pattern = xppattern

        self.data = []

        self.config = Config.getInstance()

        self.log = tb.getLogger()

    def getTree(self, url: str):
        self.log.info('Fetching: ' + url)
        response = requests.get(url, verify=self.config.args.ssl_no_verify)
        self.tree = html.fromstring(response.content)

    def getXPathChild(self, xpath: str, parent: html.HtmlElement):
        return parent.xpath(xpath)

    def getXPathElement(self, xpath: str):
        return self.getXPathChild(xpath, self.tree)

    def getXPathChildContent(self, xpath: str, parent: html.HtmlElement):
        data = []
        for elmnt in self.getXPathChild(xpath, parent):
            if isinstance(elmnt, str):
                content = elmnt
            else:
                content = ''.join(elmnt.itertext())
            content = re.sub(r'\s+', ' ', content.strip())
            data.append(content)
        content = '\n'.join(data)
        if content.isdigit():
            content = int(content)
        return content

    def getRows(self):
        return self.tree.xpath(self.pattern.row)

    def getAllData(self):
        parsed_count = 0
        for row in self.getRows():
            data = {}
            for key, xpath in self.pattern.XPathDataDict().items():
                data[key] = self.getXPathChildContent(xpath, row)
            if any(data):
                self.data.append(data)
                parsed_count += 1
        self.log.info('{} rows parsed.'.format(parsed_count))


class Scrapper:
    def __init__(self, baseurl: str, parser: XpthParser, query: dict={}):
        self.baseurl = baseurl
        self.uri = ''
        self.data = []  # ???
        self.parser = parser
        self.fetchedlinks = []
        self.query = query

        self.log = tb.getLogger()

    def get(self, uri: str):
        self.parser.getTree(uri)
        self.parser.getAllData()

    def crawl(self, uri: str):
        self.uri = uri
        if self.uri not in self.fetchedlinks:

            url = urljoin(self.baseurl, self.uri)
            scheme, netloc, path, params, query, fragment = urlparse(url)

            qs = parse_qs(query, keep_blank_values=True)

            self.log.debug('Intial query: {}'.format(str(qs)))

            qs.update(self.query)

            self.log.debug('Modified query: {}'.format(str(qs)))

            query = urlencode(qs, doseq=True)
            url = urlunparse((scheme, netloc, path, params, query, fragment))
            
            self.log.debug('Result url: {}'.format(url))

            self.get(url)
            self.fetchedlinks.append(self.uri)
            for l in self.parser.pattern.links:
                for link in self.parser.getXPathElement(l):
                    self.crawl(link)
