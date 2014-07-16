#!/usr/bin/env python
# -*- coding: utf-8 -*-
import segment

class ttitem:
   'Base class for a trip'

   def __init__(self, totalPrice = 0.0, \
                      segments = [], \
                      sellerName = u"" , \
                      travelTimeTotal = 0.0, \
                      URL = u""):
      self.totalPrice = totalPrice
      self.segments = segments
      self.sellerName = sellerName
      self.travelTimeTotal = travelTimeTotal
      self.URL = URL

   def __str__(self):
        resultString = ""
        for i in range(len(self.segments)):
            resultString += "\n" + str(self.segments[i])
        return u"ttitem:\n" + \
            u"\ttotalPrice: " + str(self.totalPrice) + u"\n" \
            u"\tsellerName: " + self.sellerName + u"\n" \
            u"\tTotal Travel Time: " + str(self.travelTimeTotal) + u"\n" \
            u"\tURL: " + self.URL + u"\n" \
            u"\tSegments: \n" + resultString
