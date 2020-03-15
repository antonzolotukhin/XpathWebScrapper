import logging
import argparse
from xpathwebscrapper.utils import Config, Toolbox


class TestConfig:
    def test_parse_args_req(self, destroyconfig):
        c = Config.getInstance()

        print(c)
        c.parse_args(["foo.yml", "bar.xlsx"])

        assert c.args.yml == "foo.yml"
        assert c.args.xlsx == "bar.xlsx"

    def test_parse_args_opt(self, destroyconfig):
        c = Config.getInstance()

        print(c)
        c.parse_args(["--ssl-no-verify", "fooo.yml", "baar.xlsx"])

        assert c.args.yml == "fooo.yml"
        assert c.args.xlsx == "baar.xlsx"
        assert c.args.ssl_no_verify is False

    def test_Config_isSingleton(self, destroyconfig):
        c1 = Config.getInstance()
        c2 = Config.getInstance()

        print(c1, c2)

        assert c1 == c2


class TestToolbox:
    def test_getLogger(self):
        assert isinstance(Toolbox.getLogger(), logging.Logger)

    def test_getArgparser(self):
        assert isinstance(Toolbox.getArgparser(), argparse.ArgumentParser)
