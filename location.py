#!/usr/bin/env python
# -*- coding: utf-8 -*-

class location:
   'Class that holds location information'

   def __init__(self, id = 0, name = u"", x = 0, y = 0):
      self.x = x
      self.y = y
      self.id = id
      self.name = name
  
   def __str__(self):
      return self.name + \
             u" [" + str(self.id) + u"] (" + str(self.x) + u"," + str(self.y) + u")"

