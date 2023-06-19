
__author__ = 'Malwareman007'
__version__ = '1.0'
__github__ = 'https://github.com/Malwareman/TechViper'
__email__ = 'malwareman007@protonmail.com'
__blog__ = 'https://techviper.webwatcher.tech/'

import importlib
import sys
import os
import platform
from datetime import datetime
class colors:
	def __init__(self):
		colors = True
		machine = sys.platform  # Detecting the os of current system
		checkplatform = platform.platform() # Get current version of OS
		if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
			colors = False  # Colors shouldn't be displayed in mac & windows
		if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
			colors = True
			os.system('')   # Enables the ANSI
		if not colors:
			end = red = white = green = yellow = run = bad = good = bold = info = que = ''
		else:
			self.white = '\033[97m'
			self.green = '\033[92m'
			self.red = '\033[91m'
			self.yellow = '\033[93m'
			self.end = '\033[0m'
			self.back = '\033[7;91m'
			self.bold = '\033[1m'
			self.blue = '\033[94m'
			self.info = '\033[93m[!]\033[0m'
			self.que = '\033[94m[?]\033[0m'
			self.bad = '\033[91m[-]\033[0m'
			self.good = '\033[92m[+]\033[0m'
			self.run = '\033[97m[~]\033[0m'
			self.grey = '\033[7;90m'
def thetime(t=None):
	now = datetime.now()
	if t:
		return now
	return f'{colors().bold}{colors().blue}[{colors().end}{colors().bold}{now.hour}:{now.minute}:{now.second}{colors().blue}{colors().bold}]{colors().end}'
class Module:
	def __init__():
		pass
	def printer(what,msg):
		if what.lower() == 'information':
			print(thetime()+f' {colors().bold}[{colors().green}INFO{colors().end}] {msg}{colors().end}')
		elif what.lower() == 'error':
			print(thetime()+f' {colors().bold}[\033[91m{colors().bold}CRITICAL{colors().end}] {colors().bold}{msg}{colors().end}')
		elif what.lower() == 'warring':
			print(thetime()+f' {colors().bold}[{colors().yellow}{colors().bold}WARRING{colors().end}] {colors().bold}{msg}{colors().end}')
		elif what.lower() == 'question':
			p = input(msg)
			if p[0].lower() == 'y' or p[0] == '':
				pass
			else:
				exit()
	def load_modules(module):
		Module.printer('info',f'Loading {module} Module')
		module = 'modules.'+module.replace('.py','').replace('/','.')
		c = importlib.import_module(module)
		return c
