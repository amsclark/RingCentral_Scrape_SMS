#import http.client
#import urllib.parse
import os,sys,time
from ringcentral import SDK
from datetime import date
from urllib.request import urlopen


rc_url = "https://platform.ringcentral.com"
# make sure that you can log in with service.ringcentral.com with the number, password, and extension you are going to use here or it won't work. Also, I believe it may need to be a privileged user in order to read all messages account-wide
rc_username = "" #number goes here. Use the country code with plus
rc_password = "" #password goes here
rc_extension = "" #extension goes here
rc_basic_auth = "Basic base64-encoded key:secret goes here"
# You'll get the clientId and secret from the developer portal credentials area for your app. 
rc_accountId = ""
rc_clientId = "" 
rc_clientSecret = ""

rcsdk = SDK(rc_clientId, rc_clientSecret, rc_url)
platform = rcsdk.platform()
platform.login(rc_username, rc_extension, rc_password)
ZIPFILE= "message_store.zip"

def create_message_store_report(rc_dateFrom, rc_dateTo, exportName):
    platform.refresh()
    print("Currently exporting " + rc_dateFrom + " to " + rc_dateTo)
    endpoint = "/restapi/v1.0/account/~/message-store-report"
    params = {
    "dateFrom": rc_dateFrom, 
    "dateTo": rc_dateTo, 
    "messageTypes": ["SMS"]
    }
    response = platform.post(endpoint, params)
    json = response.json()
    get_message_store_report_task(json.id, exportName)

def get_message_store_report_task(taskId, exportName):
    platform.refresh()
    print("check task creation status ...")
    endpoint = "/restapi/v1.0/account/~/message-store-report/" + taskId
    response = platform.get(endpoint)
    json = response.json()
    print("Task Creation Status is currently: " + json.status)
    if json.status == "Completed":
        return get_message_store_report_archive(taskId, exportName)
    else:
        time.sleep(60)
        return get_message_store_report_task(taskId, exportName)

def get_message_store_report_archive(taskId, exportName):
    print("getting report uri ...")
    endpoint = "/restapi/v1.0/account/~/message-store-report/" + taskId + "/archive"
    jsonObj = platform.get(endpoint).json()
    for i in range( len(jsonObj.records) ):
        get_message_store_report_archive_content( jsonObj.records[i].uri, i, exportName )

def get_message_store_report_archive_content(contentUri, i, exportName):
    zipFileName = f'{i}-' + exportName + ZIPFILE
    print ( f'Save report to: {zipFileName}')
    uri = platform.create_url(contentUri, False, None, True);
    fileHandler = urlopen(uri)
    with open(zipFileName, 'wb') as output:
        output.write(fileHandler.read())


# The first two parameters are the to/from date. The third parameter is a string to insert in the filename to uniquely identify it. 
# I chose to put this string in the middle after the 0/1/2 download part indicator because I wanted to easily sort to seperate the json files in the 0 file vs the mms contents.
# but if you want to change the way these are named, you can modify this string and also the "zipFileName = ..." in the first line of function get_message_store_report_archive_content
create_message_store_report("2021-03-01T00:00:00.000Z","2021-03-31T23:59:59.999Z","_2021_03_")
create_message_store_report("2021-04-01T00:00:00.000Z","2021-04-30T23:59:59.999Z","_2021_04_")
create_message_store_report("2021-05-01T00:00:00.000Z","2021-05-31T23:59:59.999Z","_2021_05_")
create_message_store_report("2021-06-01T00:00:00.000Z","2021-06-30T23:59:59.999Z","_2021_06_")
create_message_store_report("2021-07-01T00:00:00.000Z","2021-07-31T23:59:59.999Z","_2021_07_")
create_message_store_report("2021-08-01T00:00:00.000Z","2021-08-31T23:59:59.999Z","_2021_08_")
create_message_store_report("2021-09-01T00:00:00.000Z","2021-09-30T23:59:59.999Z","_2021_09_")
create_message_store_report("2021-10-01T00:00:00.000Z","2021-10-31T23:59:59.999Z","_2021_10_")
create_message_store_report("2021-11-01T00:00:00.000Z","2021-11-30T23:59:59.999Z","_2021_11_")
create_message_store_report("2021-12-01T00:00:00.000Z","2021-12-31T23:59:59.999Z","_2021_12_")

create_message_store_report("2022-01-01T00:00:00.000Z","2022-01-31T23:59:59.999Z","_2022_01_")
create_message_store_report("2022-02-01T00:00:00.000Z","2022-02-28T23:59:59.999Z","_2022_02_")
create_message_store_report("2022-03-01T00:00:00.000Z","2022-03-31T23:59:59.999Z","_2022_03_")
create_message_store_report("2022-04-01T00:00:00.000Z","2022-04-30T23:59:59.999Z","_2022_04_")
create_message_store_report("2022-05-01T00:00:00.000Z","2022-05-31T23:59:59.999Z","_2022_05_")
create_message_store_report("2022-06-01T00:00:00.000Z","2022-06-30T23:59:59.999Z","_2022_06_")
create_message_store_report("2022-07-01T00:00:00.000Z","2022-07-31T23:59:59.999Z","_2022_07_")
create_message_store_report("2022-08-01T00:00:00.000Z","2022-08-31T23:59:59.999Z","_2022_08_")
create_message_store_report("2022-09-01T00:00:00.000Z","2022-09-30T23:59:59.999Z","_2022_09_")
create_message_store_report("2022-10-01T00:00:00.000Z","2022-10-23T23:59:59.999Z","_2022_10_")

sys.exit(0)
