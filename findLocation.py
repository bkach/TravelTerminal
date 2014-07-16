import requests
import json
import codecs
import time
import datetime
import sys
import collections

reload(sys)
sys.setdefaultencoding('UTF8')

key = "9xWZV1UaopjAtfIX0nXj7HA1cekmDAKF";

def main():
    if(len(sys.argv) == 1):
        raise Exception("findLocation Needs at least one argument")
    else:
        print findLocation(sys.argv[1])

def findLocation(loc1):
    url = "https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?key=" + key + "&from=" + loc1 + "&coordSys=RT90&apiVersion=2.1"
    r = requests.get(url)
    r.encoding = 'ISO-8859-1'
    decoded = json.loads(r.text)

    results = collections.OrderedDict()
    for i in range(len(decoded['findlocationresult']['from']['location'])):
        results[decoded['findlocationresult']['from']['location'][i]['displayname']] = \
            decoded['findlocationresult']['from']['location'][i]['locationid']
        
    return results

def findLocations(loc1,loc2):
    url = "https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?key=" + key + \
        "&from=" + loc1 + \
        "&to=" + loc2 + "&coordSys=RT90&apiVersion=2.1"

    r = requests.get(url)
    r.encoding = 'ISO-8859-1'
    decoded = json.loads(r.text)

    result1 = collections.OrderedDict()
    for i in range(len(decoded['findlocationresult']['from']['location'])):
        result1[decoded['findlocationresult']['from']['location'][i]['displayname']] = \
            decoded['findlocationresult']['from']['location'][i]['locationid']

    result2 = collections.OrderedDict()
    for i in range(len(decoded['findlocationresult']['to']['location'])):
        result2[decoded['findlocationresult']['to']['location'][i]['displayname']] = \
            decoded['findlocationresult']['to']['location'][i]['locationid']

    return [result1,result2]

if  __name__ =='__main__':
    main()
