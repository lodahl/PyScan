#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:45:03 2020

@author: leif
"""
import os, json
process_name="process 3"
filename=os.path.join(os.getcwd(), 'Processes', process_name+'.json')
#filename=os.getcwd() + os.path.sep + "Processes/"+ process_name+'.json'
print(os.path.isfile(filename))
print(filename)

try:
	with open(filename) as f:
		process=f.read()
	print(process)
except:
	print("Error")	

