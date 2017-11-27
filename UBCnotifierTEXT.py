import os
from twilio.rest import Client
from urllib.request import urlopen

import re
import time
import smtplib
import getpass

#need twilio credientials to run
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]

WAIT_TIME = 30

#sends a message to 
def sendMessage(message, phonenumber):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=phonenumber,
        from_=twilio_number,
        body=message
    )

def check(url):
    response = urlopen(url).read()
    htmlText = response.decode("utf8")

    #total= re.search(totalSeats, htmlText)
    general = re.search(generalSeats, htmlText)
    restricted = re.search(restrictedSeats, htmlText)

    #print ("Total Seats: ", total.group(1))
    print("Still looking...")
    print("Restricted Seats: ", restricted.group(1))
    print("General Seats: ", general.group(1))

    if general:
        if general.group(1) != '0':
            return 1
    else:
        print("Something went wrong, maybe you put the wrong url in or lost internet connection, try restarting")
        return 0
    if restricted:
        if restricted.group(1) != '0':
            return 2
        else:
            return 0
    else:
        print("Something went wrong, maybe you put the wrong url in or lost internet connection, try restarting")
        return 0

department = input("Enter department(all caps): ")
course = input("Enter course number: ")
section = input("Enter section number: ")

#year = input("Enter year: ")
phoneNumber = input("Enter phone number:(in format +xxxxxxxxxxx) ")
restricted = input("Are restricted seats okay?(yes/no)")
print("All set, you'll recieve a text when a seat opens up :)")

#scrape data off ubc sight, without violating terms >:)
#totalSeats = re.compile("<td width=&#39;200px&#39;>Total Seats Remaining:</td><td align=&#39;left&#39;><strong>(.*?)</strong></td>")
generalSeats = re.compile("<td width=&#39;200px&#39;>General Seats Remaining:</td><td align=&#39;left&#39;><strong>(.*?)</strong></td>")
restrictedSeats = re.compile("<td width=&#39;200px&#39;>Restricted Seats Remaining\*:</td><td align=&#39;left&#39;><strong>(.*?)</strong></td>")

url = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=" + department + "&course=" + course + "&section=" + section

#check every once in a while to see if a seats available, notify you if there is!
while True:
    status = check(url)

    if status == 1:
        print("GENERAL SEAT AVAILABLE SENDING MESSAGE")
        sendMessage('There is a general seat available in ' + department + ' ' + course + '! Grab it here: ' + url, phoneNumber)
        break
    if status == 2:
        if restricted == "yes":
            print("RESTRICTED SEAT AVAILABLE")
            sendMessage('There is a restricted seat available in ' + department + ' ' + course + '! Grab it here: ' + url, phoneNumber)
            break
    else:
        time.sleep(WAIT_TIME)

