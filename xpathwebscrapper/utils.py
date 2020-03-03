import yaml
import argparse


class Config:
    __instance = None

    def __init__(self):
        if not Config.__instance:
            self.args = argparse.Namespace()
            self.yml = None

    @property
    def structure(self):
        if not self.yml:
            yml = open(self.args.yml, mode="r", encoding="utf-8-sig").read()
            self.yml = yaml.safe_load(yml)
        return self.yml

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Config()
        return cls.__instance
