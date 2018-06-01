"""Очистка XML файла от не нужных предложений, 'ТОЛЬКО СКИДКИ'"""
import requests, zipfile, io, os
import xml.etree.ElementTree as ET
import sys

name = sys.argv[1]

categorys_urls_zip = {'computer': 'http://exporter.gdeslon.ru/uploads/exports/2639de456d5f02500bb26aea0ba5810d9ad6b538.xml.zip',
                      'bit_teh': 'http://exporter.gdeslon.ru/uploads/exports/f1f0417997071cef460f9049cae1fbc9d2f72dad.xml.zip'}


r = requests.get(categorys_urls_zip[name])
zipfile = zipfile.ZipFile(io.BytesIO(r.content))
filename = zipfile.namelist()[0]
zipfile.extractall()


tree = ET.parse(filename)
root = tree.getroot()

os.remove(filename)

offers = root.find('.//offers')
offers_complet = 0
offers_delete = 0
for offer in root.findall('.//offer'):
    offers_complet += 1
    description = offer.find('description').text
    if description is None:
        offers_delete += 1
        offers.remove(offer)
        continue
    if len(description) < 150:
        offers_delete += 1
        offers.remove(offer)
        continue
    oldprice = offer.find('oldprice').text
    if oldprice is None:
        offers_delete += 1
        offers.remove(offer)
        continue

mydata = ET.tostring(root, encoding='utf-8').decode('utf-8')
myfile = open(name + "_imports.xml", "w")
myfile.write(mydata)
print('Всего:', offers_complet, 'Стер:', offers_delete, 'Осталось:', offers_complet - offers_delete)
