#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
from xpathwebscrapper.webparser import *
from xpathwebscrapper.utils import Config
import pkg_resources  # part of standart setuptools

def main():

    start = datetime.now()

    c = Config.getInstance()

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
