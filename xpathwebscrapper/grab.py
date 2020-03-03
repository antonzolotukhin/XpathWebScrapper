#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import argparse
from xpathwebscrapper.webparser import *
from xpathwebscrapper.utils import Config
import pkg_resources  # part of standart setuptools

def main():

    start = datetime.now()

    c = Config.getInstance()

    parser = argparse.ArgumentParser()

    parser.add_argument("yml", help="site_definition.yml", type=str)
    parser.add_argument("xlsx", help="result.xlsx", type=str)
    parser.add_argument("--ssl-no-verify", default=True, action='store_false', help="Turn off SSL verification")
    parser.parse_args(namespace=c.args)

    df = scrap()

    print(df)

    with pd.ExcelWriter(c.args.xlsx, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        writer.close()

    print('{} elapsed'.format(datetime.now()-start))


def scrap():

    c = Config.getInstance()

    patt = XpthPattern()
    patt.setRowXpath(c.structure.get('data',{}).get('rows'))
    patt.setXPathDataDict(c.structure.get('data',{}).get('columns',{}))
    patt.setLinks(c.structure.get('data',{}).get('links',[]))

    par = XpthParser(patt)

    scrp = Scrapper(c.structure.get('baseurl'), par, query=c.structure.get('query', {}))

    scrp.crawl(c.structure.get('starturl'))

    df = pd.DataFrame(columns=patt.DataColumns(), index=[])
    df = df.append(par.data, ignore_index=True)

    return df
