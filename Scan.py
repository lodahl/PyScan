#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 20:35:31 2020

@author: leif
"""

import json, os


class sc_process:
	'''
	Loads one process from json and extracts all paramters (in profress).
	Takes progress name as manadatory parameter and path as volounteer parameter (current librery is default)
	Returns global variables?
	'''
	def __init__(self, process, path=None):

		self.process = process
		self.path=path
		
	
		if self.path == None:
			#print(os.getcwd())
			os.chdir('Processes')
			filename=os.getcwd() + os.path.sep + self.process+'.json'
		else:
			filename=self.path + os.path.sep + self.process+'.json'
		try:
			#print(filename)
			with open(filename) as f:
				process=json.loads(f.read())
		except:	
			process=None
			print("Fejl. Filen findes ikke")
			
		os.chdir('..'+os.path.sep)
	
		self.process_name=process['process'][0]['meta']['name']
		self.process_description=process['process'][0]['meta']['description']
		self.merge_documents=process['process'][0]['meta']['merge_documents']
		self.delevery_type=process['process'][1]['delevery']['delevery_type']
		self.destination=process['process'][1]['delevery']['destination']
		self.KLe=process['process'][2]['sbsys']['KLe']
		self.SkabelonID=process['process'][2]['sbsys']['SkabelonID']
		self.documents=process['process'][3]['documents']
		
	def getProcess_name(self):
		return self.process_name
	
	def getProcess_desc(self):
		return self.process_description
	
	def getProcess_merge_documents(self):
		return self.merge_documents
	

	def __str__(self):
		return "Process: " + self.process_name + " " + self.process_description

my_process=sc_process("process 3")

print(my_process)
print(my_process.getProcess_name())
print(my_process.getProcess_desc())
print(my_process.getProcess_merge_documents())
