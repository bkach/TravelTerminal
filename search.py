#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import codecs
import time
import datetime
import sys
import segment,location,ttitem
from time import mktime
from datetime import datetime

#reload(sys)
#sys.setdefaultencoding('UTF8')

def search(location1Id, location2Id, departureDate, departureTime,
        arrivalDate, arrivalTime):
    resultFound = True
    resultNum = 0

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

        #f = codecs.open('result.json','w','utf-8')
        #f.write(json.dumps(r.json(), sort_keys=True, indent=2))
        #f.close()

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
            print str(int(trip.totalPrice)) + " sek " + \
                    datetime.fromtimestamp(mktime(currentSegment.departureTime)).strftime("%Y-%m-%d %H:%M") + "\n\t" + trip.totalTravelTime + "\n\t" + trip.URL 
        else:
            if data.keys() == [u'error']:
                print data['error']
            resultFound = False
    return trips

#cheapest = 0
#for i in range(len(trips)):
    #if (trips[i].totalPrice < trips[cheapest].totalPrice):
        #cheapest = i

#expensive = 0
#for i in range(len(trips)):
    #if (trips[i].totalPrice > trips[expensive].totalPrice):
        #expensive = i

#print "Cheapest:\n" + str(trips[cheapest])
#print "Most Expensive:\n" + str(trips[expensive])

def main():
    print "hello"

if  __name__ =='__main__':
    main()
    #print "trip " + str(i) + ": " + str(trips[i])
#for i in range(len(trips)):
    #print repr(trips[i].segments)
