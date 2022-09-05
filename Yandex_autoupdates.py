import urllib
from datetime import datetime
from threading import Thread
import time
import requests
import xml.etree.ElementTree as ET


token = ''
headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}
dowload_url = "https://online.moysklad.ru/api/yandex/market/5bf8a006-3d8e-11eb-0a80-067200018279/offer/1b7a6df7-14ba" \
              "-11ed-0a80-0ba0000e5533 "


def yml_download():
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(dowload_url, "temp.xml")



def get_json_attr():
    url = "https://online.moysklad.ru/api/remap/1.2/entity/assortment"
    response = requests.get(url=url, headers=headers)
    result = response.json()
    dict = {}
    for row in result['rows']:
            try:
                id = row['id'].replace('-', '')
                for i, el in enumerate(row['attributes']):
                    if el['name'] == 'SKU Yandex Market':
                        dict[id[0:19]] = row['attributes'][i]['value']
            except Exception:
                continue
    return dict


def replace_id():
    dict = get_json_attr()
    with open('temp.xml', encoding='utf-8') as f:
        data = f.read()
        for key in dict:
            data = data.replace(key, dict[key])
    with open('upload.xml', 'w', encoding='utf-8') as upf:
        upf.write(data)
    print('All work is done')


def main():
    yml_download()
    replace_id()


if __name__ == "__main__":
    while True:
        print(datetime.today())
        Thread(target=main()).start()
        time.sleep(1200)


# import ftplib
#
# # Fill Required Information
# HOSTNAME = "ftp-srv28164.ht-systems.ru"
# USERNAME = "srv28164"
# PASSWORD = "Eco92588"
#
# ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
#
# # force UTF-8 encoding
# ftp_server.encoding = "utf-8"
# filename = "ver2.xml"
# ftp_server.cwd("/soundliga/")
# # Read file in binary mode
# with open(filename, "rb") as file:
#     # Command for Uploading the file "STOR filename"
#     ftp_server.storbinary(f"STOR {filename}", file)


# ftp_server.quit()