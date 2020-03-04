from collections import namedtuple
from xpathwebscrapper.webparser import XpthPattern,XpthParser
from xpathwebscrapper.utils import Config
import pytest

class TestXpthPattern:

    def test_setXPathDataDict_DataColumns(inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setXPathDataDict(c.structure.get('data',{}).get('columns',{}))

        assert list(patt.DataColumns()) == ['start','finish','name','vicpart','defpart']

    def test_setRowXpath(inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setRowXpath(c.structure.get('data',{}).get('rows'))

        assert patt.row == '//table[contains(@class,\"wikitable\")]/tbody/tr[count(th)=0]'

    def test_setXPathDataDict_XPathDataDict(inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setXPathDataDict(c.structure.get('data',{}).get('columns',{}))

        assert patt.XPathDataDict() == {
                                        'start': "td[1]",
                                        'finish': "td[2]",
                                        'name': "td[3]",
                                        'vicpart': "td[4]",
                                        'defpart': "td[5]"
                                        }

    def test_setLinks(inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setLinks(c.structure.get('data',{}).get('links',[]))

        assert patt.links == ["//div[@id=\"bodyContent\"]/div[@id=\"mw-content-text\"]/div/ul/li/a[@class=\"mw-redirect\"]/@href"]
