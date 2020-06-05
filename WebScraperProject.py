from bs4 import BeautifulSoup
import bs4
import requests
from datetime import datetime
import time
import os.path
from sys import exit

#Address to check updates from
url = "https://www.gigabyte.com/Motherboard/X570-AORUS-PRO-rev-10/support#support-dl-driver"

#Define and set variables
global update, first, ver
update = False

#Check if update.txt exists (i.e. has the program been opened before) and if not, create the file
if (os.path.isfile("update.txt") == False):
    file = open("update.txt","w+")
    file.close()

#Add timestamp when printing
dateTimeObject = datetime.now();

print("[",f'{dateTimeObject.hour:02}',":",f'{dateTimeObject.minute:02}',":",f'{dateTimeObject.second:02}',"]"," Checking for updates...", sep='')

#Check the version from the last time the program was opened
file = open("update.txt","r")
ver = file.read();
file.close()

#Function for checking new version
def isNewVersion():
    #Access variables
    global update, first, ver

    #Update the update.txt file if necessary
    if (version != ver):
        ver = version
        print("\nNew version available: ",version,"\n",sep='')
        file = open("update.txt","w+")
        file.write(version)
        file.close()

    #Print the changelog
    num = 1
    print("\nChangelog:")
    for change in newest_bios.find("div", class_="div-table-cell download-desc").select("div > ol > li"):
        print(num, ". ",change.get_text().strip(),sep='')
        num += 1
    print("")

#Get the site using requests.get()
response = requests.get(url, timeout=5)

#Get the content we want from the site using BeautifulSoup
content = BeautifulSoup(response.content,"html.parser")

#Check that there were no errors
if (type(content) != BeautifulSoup):
    dateTimeObject = datetime.now();
    print("[",f'{dateTimeObject.hour:02}',":",f'{dateTimeObject.minute:02}',":",f'{dateTimeObject.second:02}',"]", sep='', end=' ')
    input("\nError: Couldn't find content on the page. It seems that the website has updated.\nPress any key to exit...")
    raise SystemExit(0)

newest_bios = content.find("div", class_="div-table-row div-table-body-BIOS")

#Check again for errors, the program crashes if the website from which the content is requested has been updated and the content we are looking for can't be found
if (type(newest_bios) != bs4.element.Tag):
    dateTimeObject = datetime.now();
    print("[",f'{dateTimeObject.hour:02}',":",f'{dateTimeObject.minute:02}',":",f'{dateTimeObject.second:02}',"]", sep='', end=' ')
    input("Error: Couldn't find content on the page. It seems that the website has updated.\nPress any key to exit...")
    raise SystemExit(0)

version = newest_bios.find("div", class_="div-table-cell download-version").get_text().strip()
download = newest_bios.find("div", class_="div-table-cell download-site").find("div", class_="hq-site").find("a").attrs
size = newest_bios.find("div", class_="div-table-cell download-size").get_text().strip()
date = newest_bios.find("div", class_="div-table-cell download-date").get_text().strip()

dateTimeObject = datetime.now();

#Print the date and time along with information on the newest version
print("[",f'{dateTimeObject.hour:02}',":",f'{dateTimeObject.minute:02}',":",f'{dateTimeObject.second:02}',"]"," Version: ",version," | Size: ",size," | Date: ",date,sep='')

#Check if the response we got has a newer version compared to the previous response and print info about the newer version
isNewVersion()

ans = input("\nDo you want to download the file? Type [y] to download, [n] to exit:")
if (ans == "y"  or ans == "Y"):
    print("\nDownloading file... don't close this window before the download has finished.")
    url = download["href"]
    r = requests.get(url)
    filename = url[url.rfind("/"):]
    dest = "C:\\Users\\Zaikou\\Desktop\\" + filename
    with open(dest, "wb") as f:
        f.write(r.content)
    print("\nDownload finished.")
    raise SystemExit(0)

elif (ans == "n" or ans == "N"):
    raise SystemExit(0)