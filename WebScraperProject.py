from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import os.path

#Address to check updates from
url = "https://www.gigabyte.com/Motherboard/X570-AORUS-PRO-rev-10/support#dl"

#Define and set variables
global update, first, ver
update = False
first = True

#Check if update.txt exists (i.e. has the program been opened before) and if not, create the file
if (os.path.isfile("update.txt") == False):
    file = open("update.txt","w+")
    file.close()

#Check the version from the last time the program was opened
file = open("update.txt","r")
ver = file.read();
file.close()

#Function for checking new version
def isNewVersion():
    #Access variables
    global update, first, ver

    #Print the changelog when the program is opened, but not again unless there is a new version and update the update.txt file
    if (version != ver):
        ver = version
        print("\nNew version: ",version,sep='')
        file = open("update.txt","w+")
        file.write(version)
        file.close()
    if(first == True):
        num = 1
        print("\nChangelog:")
        for change in newest_bios.find("div", class_="div-table-cell download-desc").select("div > ol > li"):
            print(num, ". ",change.get_text().strip(),sep='')
            num += 1
        print("")
        first = False

#Infinite loop to keeping the program running
while (True):
    #Get the site using requests.get()
    response = requests.get(url, timeout=5)

    #Get the content we want from the site using BeautifulSoup
    content = BeautifulSoup(response.content,"html.parser")
    newest_bios = content.find("div", class_="div-table-row div-table-body-BIOS")
    version = newest_bios.find("div", class_="div-table-cell download-version").get_text().strip()
    size = newest_bios.find("div", class_="div-table-cell download-size").get_text().strip()
    date = newest_bios.find("div", class_="div-table-cell download-date").get_text().strip()

    #Add timestamp when printing
    dateTimeObject = datetime.now();

    #Print the date and time along with information on the newest version
    print("[",dateTimeObject.day,".",dateTimeObject.month,".",dateTimeObject.year," ",f'{dateTimeObject.hour:02}',":",f'{dateTimeObject.minute:02}',":",f'{dateTimeObject.second:02}',"]"," Version: ",version," | Size: ",size," | Date: ",date,sep='')

    #Check if the response we got has a newer version compared to the previous response and print info about the newer version
    isNewVersion()

    #Wait for a certain time until the next refresh
    time.sleep(3600)