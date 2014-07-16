#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import codecs
import time
import datetime
import sys

sys.path.insert(0,'./classes')
import segment,location,ttitem

reload(sys)
sys.setdefaultencoding('UTF8')

# API Key
key = "9xWZV1UaopjAtfIX0nXj7HA1cekmDAKF";
location1Name = "uppsala centralstation"
location2Name = "malmö centralstation"

def getLocation(name, attribute='displayname'):
    url = "https://api.trafiklab.se/samtrafiken/resrobot/FindLocation.json?key=" + key + "&from=" + name + "&coordSys=RT90&apiVersion=2.1"
    r = requests.get(url)
    r.encoding = 'ISO-8859-1'
    decoded = json.loads(r.text)
    return decoded['findlocationresult']['from']['location'][0][attribute]
    
location1Id = getLocation(location1Name, "locationid")
location2Id = getLocation(location2Name, "locationid")

now = datetime.datetime.now()
departureDate = now.strftime("%Y-%m-%d")
departureTime = now.strftime("%H:%M")

one_day = datetime.timedelta(weeks=1)
later = now + one_day

arrivalDate = later.strftime("%Y-%m-%d")
arrivalTime = later.strftime("%H:%M")

#print departureDate
resultFound = True
resultNum = 0

output = codecs.open('output','w','utf-8')

trips = []

while(resultFound):

    r = requests.get("http://www.yathra.se/finder.php?" + \
            "avgnr=" + str(resultNum) + "&" +  \
            "from=" + location1Id + "&" + \
            "to=" + location2Id + "&" + \
            "departureDate=" + departureDate + "&" + \
            "departureTime=" + departureTime + "&" + \
            "arrivalDate=" + arrivalDate + "&" + \
            "arrivalTime=" + arrivalTime)
    r.encoding = 'ISO-8859-1'

    f = codecs.open('result.json','w','utf-8')
    f.write(json.dumps(r.json(), sort_keys=True, indent=2))
    f.close()

    data = json.loads(r.text)


    if (data.keys() != [u'error']):
        for i in range (len(data['timetableresult']['ttitem'])):

            trip = ttitem.ttitem()
            trip.totalPrice = float(data['timetableresult']['ttitem'][i]['price'])
            trip.sellerName = data['timetableresult']['ttitem'][i]['sellername']
            trip.totalTravelTime = data['timetableresult']['ttitem'][i]['traveltimetotal']
            trip.URL = data['timetableresult']['ttitem'][i]['url']
            trip.segments = []

            for j in range (len(data['timetableresult']['ttitem'][i]['segment'])):
                currentSegment = segment.segment()
                currentSegment.arrivalTime = \
                    time.strptime(data['timetableresult']['ttitem'][i]['segment'][j]['arrival']['datetime'], \
                        "%Y-%m-%d %H:%M")
                currentSegment.arrivalLocation = location.location(
                         data['timetableresult']['ttitem'][i]['segment'][j]['arrival']['location']['id'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['arrival']['location']['name'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['arrival']['location']['x'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['arrival']['location']['y'] \
                         )
                currentSegment.departureTime = \
                    time.strptime(data['timetableresult']['ttitem'][i]['segment'][j]['departure']['datetime'], \
                        "%Y-%m-%d %H:%M")
                currentSegment.departureLocation = location.location(
                         data['timetableresult']['ttitem'][i]['segment'][j]['departure']['location']['id'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['departure']['location']['name'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['departure']['location']['x'], \
                         data['timetableresult']['ttitem'][i]['segment'][j]['departure']['location']['y'] \
                         )
                if('direction' in data['timetableresult']['ttitem'][i]['segment'][j].keys()):
                    currentSegment.direction = data['timetableresult']['ttitem'][i]['segment'][j]['direction']
                currentSegment.lowestPrice = data['timetableresult']['ttitem'][i]['segment'][j]['lowestprice']
                currentSegment.lowestPriceCompany = data['timetableresult']['ttitem'][i]['segment'][j]['lowestpriceseller']['name']
                currentSegment.lowestPriceURL = data['timetableresult']['ttitem'][i]['segment'][j]['lowestpriceseller']['url']
                currentSegment.segmentNumber = j
                trip.segments.append(currentSegment)
            trips.append(trip)
        resultNum += 1
        print "ResultNum " + str(resultNum) + " " + str(currentSegment.departureTime)
    else:
        if data.keys() == [u'error']:
            print data['error']
        resultFound = False

cheapest = 0
for i in range(len(trips)):
    if (trips[i].totalPrice < trips[cheapest].totalPrice):
        cheapest = i

expensive = 0
for i in range(len(trips)):
    if (trips[i].totalPrice > trips[expensive].totalPrice):
        expensive = i

print "Cheapest:\n" + str(trips[cheapest])
print "Most Expensive:\n" + str(trips[expensive])

def main():
    print "hello"

if  __name__ =='__main__':
    main()
    #print "trip " + str(i) + ": " + str(trips[i])
#for i in range(len(trips)):
    #print repr(trips[i].segments)
