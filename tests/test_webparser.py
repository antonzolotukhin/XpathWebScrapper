from xpathwebscrapper.webparser import XpthPattern, XpthParser
from xpathwebscrapper.utils import Config
from lxml import etree, html


class TestXpthPattern:
    def test_setXPathDataDict_DataColumns(self, inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setXPathDataDict(c.structure.get("data", {}).get("columns", {}))

        assert list(patt.DataColumns()) == ["start", "finish", "name", "vicpart", "defpart"]

    def test_setRowXpath(self, inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setRowXpath(c.structure.get("data", {}).get("rows"))

        assert patt.row == '//table[contains(@class,"wikitable")]/tbody/tr[count(th)=0]'

    def test_setXPathDataDict_XPathDataDict(self, inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setXPathDataDict(c.structure.get("data", {}).get("columns", {}))

        assert patt.XPathDataDict() == {
            "start": "td[1]/text()",
            "finish": "td[2]/text()",
            "name": "td[3]",
            "vicpart": "td[4]",
            "defpart": "td[5]",
        }

    def test_setLinks(self, inittestconfig):
        c = Config.getInstance()

        patt = XpthPattern()
        patt.setLinks(c.structure.get("data", {}).get("links", []))

        assert patt.links == [
            '//div[@id="bodyContent"]' + '/div[@id="mw-content-text"]' + '/div/ul/li/a[@class="mw-redirect"]/@href'
        ]


class TestXpthParser:
    def test_getTree(self, inittestconfig, httpget_mock):
        par = XpthParser(XpthPattern())
        par.getTree("https://py.testopedia.org/tree.html")
        h = b"""<html>\n<body>\n<p>this is test</p>\n</body>\n</html>"""

        assert isinstance(par.tree, html.HtmlElement)
        assert etree.tostring(par.tree) == h

    def test_getXPathChild(self, inittestconfig):
        par = XpthParser(XpthPattern())
        h = b"""<html><body><p>p1</p><p>p2</p></body></html>"""
        t = html.fromstring(h)
        e = par.getXPathChild("//body/p", t)

        assert len(e) == 2
        assert etree.tostring(e[0]) == b"<p>p1</p>"
        assert etree.tostring(e[1]) == b"<p>p2</p>"

    def test_getXPathChildContent(self, inittestconfig):
        par = XpthParser(XpthPattern())
        h = b"""<html><body><p>test1  </p><p>test2<br/>\ntest3</p>   test4</body></html>"""
        t = html.fromstring(h)
        e = par.getXPathChildContent("//body", t)

        assert e == "test1 test2 test3 test4"
