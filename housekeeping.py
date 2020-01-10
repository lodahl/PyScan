#!/usr/bin/python3

import os

def cleanup_temp(path):
	'''
	Deletes all files in a folder.
	Takes a path as parameter
	'''
	if os.path.exists(path):
		files=os.listdir(path)
		for file in files:
			#print(file)
			os.remove(path+ os.path.sep + file)

def create_temp(path):
	'''
	If the temporary folder doesn't exist its created.
	Takes a path as parameter
	'''
	if not os.path.exists(path):
		os.makedirs(path)
