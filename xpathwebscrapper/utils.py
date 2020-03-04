import yaml
import argparse
import logging


class Config:
    __instance = None

    def __init__(self):
        if not Config.__instance:
            self._args = None
            self._yml = None
            self.argparser = Toolbox.getArgparser()

    def parse_args(self,args=None):
        """ Можно вызвать как .parse_args(['--ssl_no_verify', 'def.yml', 'out.xlsx'])
            или без аргументов: .parse_args() - тогда аргументы будут взяты из коммандной строки
        """
        self._args = self.argparser.parse_args(args)

    @property
    def args(self):
        if not self._args:
            self.parse_args()
        return self._args

    @property
    def structure(self):
        if not self._yml:
            yml = open(self.args.yml, mode="r", encoding="utf-8-sig").read()
            self._yml = yaml.safe_load(yml)
        return self._yml

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Config()
        return cls.__instance

class Toolbox:
    argparser = None
    logger = None
    lhandler = None
    lformater = None

    @classmethod
    def getLogger(cls):
        if not cls.logger:
            logging.captureWarnings(True)
            cls.logger = logging.getLogger(__name__)
            cls.logger.setLevel(logging.DEBUG)

            cls.lhandler = logging.StreamHandler()

            cls.lformater = logging.Formatter('[%(levelname)s]: %(message)s')
            cls.lhandler.setFormatter(cls.lformater)

            cls.logger.addHandler(cls.lhandler)

        return cls.logger

    @classmethod
    def getArgparser(cls):
        if not cls.argparser:
            cls.argparser = argparse.ArgumentParser()
            cls.argparser.add_argument("yml", help="site_definition.yml", type=str)
            cls.argparser.add_argument("xlsx", help="result.xlsx", type=str)
            cls.argparser.add_argument("--ssl-no-verify", default=True, action='store_false', help="Turn off SSL verification")
        return cls.argparser
