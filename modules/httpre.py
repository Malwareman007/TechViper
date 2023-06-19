#!/usr/bin/env python3
from modules.techviper import Module,colors,thetime
def data(): # The all data of module
	data = {
	'name': 'httpre',
	'description':'''
Get a live subdomains
	''',
	'date':'18-06-2023',
	'license':'MIT',
	'authors':[
	'Malwareman007'],
	'emails':[
	'Malwareman007@protonmail.com'],
	'list_support': True,
	'options':[
	'url',
	'threads',
	'timeout'
	]
	}
	return data
class script:
	def __init__(self):
		global q
		from queue import Queue
		q = Queue()
	def threader():
		item = q.get()
		script.opener(item)
		q.task_done()
	def opener(domain):
		import requests
		try:
			r = requests.get(f'http://{domain.strip()}',timeout=timeout,verify=False,allow_redirects=False)
			print(f'{colors().good} Live : {domain.strip()}')
			f = open(name,'a')
			f.write(f'\nhttp://{domain.strip()}')
			f.close()
		except:
			print(f'{colors().bad} {domain.strip()}')
	def run(self,options):
		global timeout,name
		import os
		name = f'{os.getcwd()}/TecchViper_done_{thetime(t="yes").second}_{thetime(t="yes").minute}.txt'
		timeout = options['timeout']
		from threading import Thread
		for thr in range(options['threads']):
			p1 = Thread(target=script.threader)
			p1.daemon = True
			p1.start()
		for url in options['file']:
			q.put(url.strip())
		q.join()
