import pandas as pd
from datetime import datetime
from  webparser import *
import yaml
import argparse

start=datetime.now()

# конфигурируем ArgumentParser
parser = argparse.ArgumentParser()
# по-умолчанию запрашиваем issues у юзера devopshq
parser.add_argument("yml", type=str)

args = parser.parse_args()

structure = yaml.safe_load(open(args.yml).read())

patt = XpthPattern()
patt.setRowXpath(structure.get('data').get('rows'))
patt.setXPathDataDict(structure.get('data').get('columns'))
patt.setLinks(structure['data']['links'])

par = XpthParser(patt)

scrp = Scrapper(structure.get('baseurl'),par)

d = scrp.crawl(structure.get('starturl'))


df = pd.DataFrame(columns=patt.DataColumns(), index=[])
df=df.append(par.data, ignore_index=True)

print (df)

with pd.ExcelWriter('reestr.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer,sheet_name='Реестр ПО',index=False)
    writer.save()
    writer.close()
#       ---

print ('{} elapsed'.format(datetime.now()-start))
