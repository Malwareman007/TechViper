#!/usr/bin/env python3
from modules.techviper import Module,colors
def data(): # The all data of module
	data = {
	'name': 'port scanning',
	'description':'''
Make Port scanning processe using Hackertarget api
With This module you can scan all hosts using NMAP Tool Online
	''',
	'date':'18-06-2023',
	'license':'MIT',
	'authors':[
	'Malwareman007'],
	'emails':[
	'Malwareman007@protonmail.com'],
	'list_support': False,
	'options':[
	'url'
	]
	}
	return data
class script:
	def __init__(self):
		pass
	def run(self,options):
		import requests
		r = requests.get('https://api.hackertarget.com/nmap/?q='+options['url'].split('/')[2])
		print(r.text)
