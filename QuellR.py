#!/usr/bin/env python3

"""
This is QuellR. A means to decode to detonate QR codes 
before they hit a mailbox.

Needs: 
 - CTI API Connectivity
 - Connectivity to mail client
"""


import requests
import os
import subprocess
import re
import glob
import cv2
import pathlib
from unshortenit import UnshortenIt


os.chdir('/opt/Jupyter_Notebooks/QuellR') # Change this to your directory of choice
with open("shorteners.txt", "r") as url_shorteners:
    #shortners_list = url_shorteners.read().splitlines()
    shortners_list = set(line.strip() for line in url_shorteners)
url_shorteners.close()
print(shortners_list)
global domains
domains = []

def qr_decode(f):
    # qr = read_qr_code(f)
    DFRAME = pd.DataFrame(columns=['File_Name', 'URL', 'OTX', 'VirusTotal', 'Shodan'])
    f = cv2.imread(f)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(f)
    value1 = re.sub("http\:\/\/", "", str(value))
    value1 = re.sub("https\:\/\/", "", str(value1))
    value1 = re.sub("\/\S+", "", str(value1))
    value = str(value)
    value1 = str(value1)
    http = 'http://'
    if len(value) > 0:
        if http not in value:
            value = str(http + value)
        if value1 in shortners_list:
            unshortener = UnshortenIt()
            web_host = unshortener.unshorten(value)
            domains.append(web_host)
        else:
            web_host = value
            domains.append(web_host)
            

#directory = input("Enter the directory of the QR codes:")
directory = "/opt/Jupyter_Notebooks/QuellR/QRs"
os.chdir(directory)
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        qr_decode(f)
for d in domains:
    print(d)