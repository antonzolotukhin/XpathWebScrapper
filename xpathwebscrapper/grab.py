#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import yaml
import argparse
from xpathwebscrapper.webparser import *
import pkg_resources  # part of standart setuptools

def main():

    start = datetime.now()

    # конфигурируем ArgumentParser
    parser = argparse.ArgumentParser()

    parser.add_argument("yml", help="site_definition.yml", type=str)
    parser.add_argument("xlsx", help="result.xlsx", type=str)
    args = parser.parse_args()

    df = scrap(args.yml)

    print(df)

    with pd.ExcelWriter(args.xlsx, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=args.xlsx, index=False)
        writer.save()
        writer.close()

    print('{} elapsed'.format(datetime.now()-start))


def scrap(ymlfile: str):

    yml = open(ymlfile, mode="r", encoding="utf-8-sig").read()
    structure = yaml.safe_load(yml)

    patt = XpthPattern()
    patt.setRowXpath(structure.get('data',{}).get('rows'))
    patt.setXPathDataDict(structure.get('data',{}).get('columns',{}))
    patt.setLinks(structure.get('data',{}).get('links',[]))

    par = XpthParser(patt)

    scrp = Scrapper(structure.get('baseurl'), par, query=structure.get('query', {}))

    d = scrp.crawl(structure.get('starturl'))

    df = pd.DataFrame(columns=patt.DataColumns(), index=[])
    df = df.append(par.data, ignore_index=True)

    return df
