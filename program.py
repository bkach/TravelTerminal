from findLocation import findLocation
import sys
import datetime
import time
from search import search
from time import mktime
from datetime import datetime

reload(sys)
sys.setdefaultencoding('UTF8')

def printResults(results,start,num):
    if(num > len(results.items()) - 1):
        num = len(results.items()) - 1
    elif(start < len(results.items()) - 1):
        for i in range(start,num):
            print str(i) + ": " + \
            unicode(results.items()[i][0]).encode('utf-8')
    else:
        print "No More Results"

def station_choice(results,num):
    choice = raw_input("Station Number: ")
    if choice == "":
        printResults(results,num,num+10)
        return station_choice(results,num+10)
    elif int(choice) < 0 or int(choice) >= num:
        print "Out of bounds"
        return station_choice(results,num)
    else:
        return choice
if len(sys.argv) == 1:
    from_station = raw_input("From: Stockholm" + chr(8)*9)
    if not from_station:
        from_station = "Stockholm"
    from_results = findLocation(from_station)
    printResults(from_results,0,10)
    from_choice = int(station_choice(from_results,10))
    from_choice_name = from_results.items()[from_choice][0]
    from_choice_id = from_results.items()[from_choice][1]
    print "\t" + unicode(from_choice_name).encode('utf-8')


    to_station = raw_input("To: Uppsala" + chr(8)*4)
    if not to_station:
        to_station = "Uppsala"
    to_results = findLocation(to_station)
    printResults(to_results,0,10)
    to_choice = int(station_choice(to_results,10))
    to_choice_name = to_results.items()[to_choice][0]
    to_choice_id = to_results.items()[to_choice][1]
    print "\t" + unicode(to_choice_name).encode('utf-8')

    departureDate = raw_input("Departure Window Date : %s" \
            % datetime.now().strftime("%Y-%m-%d") + chr(8)*10)
    if not departureDate:
        departureDate = datetime.now().strftime("%Y-%m-%d")
    departureTime = raw_input("Departure Window Time: %s" \
            % datetime.now().strftime("%H:%M") + chr(8)*5)
    if not departureTime:
        departureTime = datetime.now().strftime("%H:%M")
    arrivalDate = ""
    while arrivalDate == "":
        arrivalDate = raw_input("Arrival Window Date (%s): " \
                % datetime.now().strftime("%Y-%m-%d"))
    arrivalTime = ""
    while arrivalTime == "":
        arrivalTime = raw_input("Arrival Window Time (%s): " \
                % datetime.now().strftime("%H:%M"))

    trips = search(from_choice_id, to_choice_id, departureDate, departureTime,
        arrivalDate, arrivalTime)
else:
    trips = search(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

cheapest_choice = raw_input("Cheapest? y/n ")
if cheapest_choice == "y":
    print
    cheapest = 0
    for i in range(len(trips)):
        if (trips[i].totalPrice < trips[cheapest].totalPrice):
            cheapest = i
    print str(int(trips[cheapest].totalPrice)) + " sek " + \
datetime.fromtimestamp(mktime(trips[cheapest].segments[0].departureTime )).strftime("%Y-%m-%d %H:%M") + "\n\t" + trips[cheapest].URL 

#time_choice = raw_input("Shortest Time? y/n")
#if time_choice == "y":
    #cheapest = 0
    #for i in range(len(trips)):
        #if (trips[i].totalPrice < trips[cheapest].totalPrice):
            #cheapest = i
