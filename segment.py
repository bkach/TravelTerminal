#!/usr/bin/env python
# -*- coding: utf-8 -*-

import location

class segment:
   'A segment of a trip (or a leg)'

   def __init__(self, \
                arrivalTime = 0, \
                arrivalLocation = location.location(), \
                departureTime = 0, \
                departureLocation = location.location,
                direction = u"", \
                lowestPrice = 0.0, \
                lowestPriceCompany = u"", \
                lowestPriceURL = u"", \
                segmentNumber = 0):
    self.arrivalTime = arrivalTime
    self.arrivalLocation = arrivalLocation
    self.departureTime = departureTime
    self.departureLocation = departureLocation
    self.direction = direction
    self.lowestPrice = lowestPrice
    self.lowestPriceCompany = lowestPriceCompany
    self.lowestPriceURL = lowestPriceURL
    self.segmentNumber = segmentNumber

   def __str__(self):
      return u"\tSegment " + str(self.segmentNumber) + u":\n" + \
         u"\t\tarrivalTime : " + str(self.arrivalTime) + u"\n" + \
         u"\t\tarrivalLocation: " + str(self.arrivalLocation) + u"\n" + \
         u"\t\tdepartureTime : " + str(self.departureTime) + u"\n" \
         u"\t\tdepartureLocation: " + str(self.departureLocation) + u"\n" + \
         u"\t\tdirection: " + self.direction + u"\n" + \
         u"\t\tlowestPrice: " + str(self.lowestPrice) + u"\n" + \
         u"\t\tlowestPriceCompany: " + self.lowestPriceCompany + u"\n" + \
         u"\t\tlowestPriceURL: " + self.lowestPriceURL + u"\n" \
