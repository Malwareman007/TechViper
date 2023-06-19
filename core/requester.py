__author__ = 'Malwareman007'
__version__ = '1.0'
__github__ = 'https://github.com/Malwareman007/TechViper'
__email__ = 'Malwareman007@protonmail.com'
__blog__ = 'https://techviper.webwatcher.tech' 

from datetime import datetime
from .colors import *
from .config import *
from .logger import logger
from .scanner import uagent
from time import sleep
import requests,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def thetime():
	now = datetime.now()
	return f'{bold}{blue}[{end}{bold}{now.hour}:{now.minute}:{now.second}{blue}{bold}]{end}'
def red(w):
	if w == 'ag':
		return True
	else:
		return False
def con(url,redir,cookie=None,timeo=None,vert=None,proxy=None,slp=0,cagent=None):
	try:
		if slp != 0:
			logger.debug(f'Sleeping {slp} sec')
		sleep(slp)
		logger.info(f'Check The URL')
		r = requests.get(url,allow_redirects=redir,timeout=timeo,cookies=cookie,verify=vert,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
		if r.status_code == 200:
			logger.info(f'http response : {r.status_code}')
		elif r.status_code == 302 or r.status_code == 301:
			logger.info(f"http response : {r.status_code} That's mean Redirect to another page/website")
		elif r.status_code == 999:
			logger.info('KingWaf Firwill Has been detected')
			sleep(1)
		else:
			logger.info(f'http response : {r.status_code}')
	except requests.exceptions.ConnectionError:
		logger.error(f"host '{blue}{url}{end}' does not exist ..!")
		exit()
	except requests.exceptions.ReadTimeout:
		logger.error(f"\n{bad} Timeout Error ")
		exit()
	except requests.exceptions.ProxyError:
		logger.error(f"{bad} Proxy Connection Error")
		exit()
	except requests.exceptions.InvalidURL:
		logger.error(f"{bad} Invalid URL")
		exit()
	except requests.exceptions.InvalidSchema:
		logger.error(f"{bad} Invalid Schame")
		exit()
	except requests.exceptions.MissingSchema:
		logger.error(f"{bad} Missing Schema")
		exit()
def con_f(url,redir,cookie=None,timeo=None,vert=None,proxy=None,cagent=None,slp=0):
	try:
		sleep(slp)
		r = requests.get(url,allow_redirects=redir,timeout=timeo,verify=vert,cookies=cookie,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
		return 'ok'
	except requests.exceptions.ReadTimeout:
		return 'no','\ntimeout error ..'
	except requests.exceptions.ConnectionError:
		return 'no','Connection Error ..'
	except requests.exceptions.ProxyError:
		return 'no','Proxy Connection Error'
	except requests.exceptions.InvalidURL:
		return 'no','Invalid URL'
	except requests.exceptions.InvalidSchema:
		return 'no','Invalid Schema'
	except requests.exceptions.MissingSchema:
		return 'no','Missing Schema'
