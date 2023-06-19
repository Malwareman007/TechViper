
__author__ = 'Malwareman'
__version__ = '1.0'
__github__ = 'https://github.com/Malwareman/TechViper'
__email__ = 'malwareman007@gmail.com'
__blog__ = 'https://techviper.webwatcher.tech/'

import time,sys,os,re,threading
from core.scanner import *
from core.colors import *
from core.requester import *
from core.logger import logger
from modules.techviper import Module
from optparse import OptionParser
from queue import Queue
def post_data(params):
    if params:
        prePostData = params.split("&")
        postData = {}
        for d in prePostData:
            p = d.split("=", 1)
            postData[p[0]] = p[1]
        return postData
    return {}
def getargs():
	global the_options,url,froms,data,rfile,r,cookie,thr,timeo,date,encoded,redir,vert,cagent,proxy,sleep,yeh,nopar,modulee,module,d,batch
	modulee = False
	rfile = None
	yeh = False
	url = None
	proxy = None
	cookie = None
	nopar = False
	r=False
	helper=("""
Options:
  -h, --help          |    Show help message and exit
  --version           |    Show program's version number and exit
  -u URL, --url=URL   |    Target URL (e.g."http://www.target.com/vuln.php?id=1")
  --data=DATA         |    Data string to be sent through POST (e.g. "id=1")
  --list=FILE         |    Get All Urls from List
  --threads           |    Max number of concurrent HTTP(s) requests (default 10)
  --timeout           |    Seconds to wait before timeout connection
  --proxy             |    Start The Connection with http(s) proxy
  --cookies           |    HTTP Cookie header value (e.g. "PHPSESSID=a8d127e..")
  --encode            |    How Many encode the payload (default 1)
  --allow-redirect    |    Allow the main redirect
  --verify            |    Skip HTTPS Cert Error
  --user-agent        |    add custom user-agent
  --scan-headers      |    Try to inject payloads in headers not parameters (user-agent,referrer)
  --skip-headers      |    Skip The Headers scanning processe
  --sleep             |    Sent one request after some Seconds
  --batch             |    Never ask for user input, use the default behavior
  --module            |    add custom module (e.g. "google.py")
	""")
	optp = OptionParser(add_help_option=False)
	optp.add_option("-u","--url",dest="url",help='Target URL (e.g. "http://www.target.com/vuln.php?id=1")')
	optp.add_option("--data",dest="data",help='Data string to be sent through POST (e.g. "id=1")')
	optp.add_option("-h","--help",dest="help",action='store_true',help="Show Help Menu")
	optp.add_option("--list",dest="rfile",help="Get All Urls from file ..")
	optp.add_option("--threads",type='int',dest="thread",help='Thread number ..(DEF : 10)')
	optp.add_option("--timeout",type='int',dest="timeo",help="Set Timeout")
	optp.add_option("--cookies",dest='cookie',help='Add cookie in Request')
	optp.add_option("--encode",type="int",dest="encoded",help='How Many encode the payload')
	optp.add_option("--version",dest='ver',action='store_true')
	optp.add_option("--allow-redirect",dest='redirect',action='store_true')
	optp.add_option("--verify",dest="vert",action="store_true")
	optp.add_option("--user-agent",dest='cagent')
	optp.add_option("--proxy",dest='proxy')
	optp.add_option("--sleep",dest='sleep',type='int')
	optp.add_option("--module",dest='module')
	optp.add_option("--skip-headers",dest='yeh',action='store_true')
	optp.add_option("--scan-headers",dest='nopar',action='store_true')
	optp.add_option('--batch',dest='batch',action='store_true')
	opts, args = optp.parse_args()
	if opts.help:
		print(helper)
		exit()
	if opts.batch:
		batch = True
	else:
		batch = False
	if opts.proxy:
		proxy = opts.proxy
		if proxy.startswith("http://"):
			proxy = {'http':proxy}
		elif proxy.startswith("https://"):
			proxy = {'https':proxy}
		elif proxy.startswith('http://') == False and proxy.startswith('https://') == False:
			logger.error("This Proxy Not Supported from TechViper")
			exit()
		else:
			logger.error("Please add the protocol of the proxy like this (`{grey}--proxy='http://127.0.0.1:8080'{end}`)")
			exit()
	else:
		proxy = None
	if opts.nopar:
		nopar = True
	else:
		nopar = False
	if opts.yeh:
		yeh = True
	if nopar == True and yeh == True:
		logger.error("You can't start with `--skip-headers` and `--scan-headers` at same time ..")
		exit()
	if opts.sleep:
		sleep = opts.sleep
		try:
			time.sleep(sleep)
		except ValueError:
			logger.error('sleep length must be non-negative')
			exit()
	else:
		sleep = 0
	if opts.cagent:
		logger.info('Loading Your Custom User-agent')
		cagent = opts.cagent
		cagent = cagent.replace("<",'').replace(">",'').replace('{','').replace("}",'').replace("<%",'').replace('%>','').replace("'",'').replace('"','').replace("|",'')
	else:
		cagent = None
	if opts.thread:
		thr = opts.thread
	else:
		thr = 10
	if opts.redirect:
		redir = False
	else:
		redir = True
	if opts.url:
		url=opts.url
		url=url.replace("'",'').replace('"','')
		url=url.replace("{",'').replace("}",'')
		url=url.replace("<%",'').replace("%>",'')
		url=url.replace("<",'').replace(">",'').replace("|",'')
		if url.startswith('http://') or url.startswith('https://'):
			pass
		else:
			url = 'http://'+url
		logger.info(f'Loading The Target : {url.split("/")[2]}')
	if opts.vert:
		vert = True
	else:
		vert = False
	if opts.url == None and opts.rfile != None:
		rfile=str(opts.rfile)
		r = True
		url = None
	if opts.encoded:
		encoded = opts.encoded
		logger.info(f'Encoding The Payload : {encoded}')
		if encoded > 10:
			logger.error("maximum number of used encode is 10 avoiding potential issues")
			exit()
	else:
		encoded = 1
	if opts.data:
		date = opts.data
		try:
			date = post_data(date)
			logger.info('Loading data For post request')
		except:
			logger.critical("Invild Params .. Please add data like (--data='id=1&search=55')")
			time.sleep(1)
			exit()
	else:
		date = None
	if opts.timeo:
		timeo = opts.timeo
		logger.info(f'Loading Timeout : {timeo}')
	else:
		timeo = None
	if opts.rfile != None and date != None:
		logger.critical(f"You Can't Add Post request using \033[7;96m--data='\033[9;94m{opts.data}{end}' with list file ..")
		time.sleep(1)
		exit()
	if opts.help:
		print(helper)
		exit()
	if opts.ver:
		print(__version__)
		exit()
	if opts.url != None and opts.rfile != None:
		logger.error("You Can't Start TechViper With List option and url option ")
		exit()
	if opts.cookie:
		cookie=str(opts.cookie)
		try:
			cookie=post_data(cookie)
			logger.info('Loading The Cookies')
		except:
			logger.error('Invild Cookies ..')
			exit()
	else:
		cookie=None
	if opts.module:
		modulee = True
		module = opts.module.replace('.py','')
		logger.info(f'Loading {module} Module')
		try:
			module = Module.load_modules(module)
		except:
			logger.error('ImportError')
			exit()
		logger.info('Checking The Module')
		time.sleep(1)
		try:
			d = module.data()
			name = d['name']
			description = d['description']
			date = d['date']
			license = d['license']
			authors = d['authors']
			emails = d['emails']
			script_options = d['options']
			if name == None or description == None or date == None or emails == None or authors == None:
				logger.error('i need more informations abount module please read the developers docs on TechViper website')
				exit()
			email = ''
			author = ''
			for i in emails:
				email += i+', '
			for i in authors:
				author += i+', '
			logger.info('Module Loading successfully')
			print(f"""\n
\033[91m#{yellow}{bold}{'-'*50}{end}\033[91m#{end}
	   {bold}\033[91m|{end}{bold} Module Informations \033[91m|{end}
	   {bold}\033[91m{'-'*23}{end}
{bold}{info}{bold} Name    : {name}
{bold}{info}{bold} Date    : {date}
{bold}{info}{bold} License : {license}
{bold}{info}{bold} Authors : {author}
{bold}{info}{bold} Emails  : {email}
\033[91m#{yellow}{bold}{'-'*50}{end}\033[91m#{end}
{bold}\033[91m{end} Description \033[91m|{end}
{bold}{yellow}#\033[91m{'-'*23}{end}{yellow}#{end}
{description}
{bold}{yellow}#\033[91m{'-'*23}{end}{yellow}{bold}#{end}
""")
			modulee = True
			module_options = {
			'url':url,
			'cookies':cookie,
			'proxy':proxy,
			'threads':thr,
			'timeout':timeo,
			'timeout*':timeo,
			'threads*':thr,
			'url*':url,
			'cookies*':cookie,
			'proxy*':proxy,
			}
			the_options = {}
			for option in script_options:
				the_options[option] = module_options[option]
			try:
				for o,v in the_options.items():
					if o[-1] == '*':
						if v == None:
								logger.error(f'Module Errors . i need this option ({o})for continue')
								exit()
				for o,v in the_options.items():
					the_options[o.replace('*','')] = the_options.pop(o)
			except KeyError:
				logger.error('Module Errors . This Value ({o.replace("*","")})Not Supported ')
				exit()
		except:
			logger.error('Module Errors (informations)')
			exit()
	if opts.url == None and opts.rfile == None and opts.help == None:
		optp.error('missing a mandatory option (--url,--cookies,--data,--list,--encode) Use -h for help ..!')
		exit()
def logo():
	l=(f'''\033[1;92m
  ::::::::::::::::::::::::::::: :::    ::: 
     :+:    :+:      :+:    :+::+:    :+:  
    +:+    +:+      +:+       +:+    +:+   
   +#+    +#++:++# +#+       +#++:++#++    
  +#+    +#+      +#+       +#+    +#+     
 #+#    #+#      #+#    #+##+#    #+#      
###    ################## ###    ###       
          
\033[1;97m
   :::     ::::::::::::::::::::::: ::::::::::::::::::: 
  :+:     :+:    :+:    :+:    :+::+:       :+:    :+: 
 +:+     +:+    +:+    +:+    +:++:+       +:+    +:+  
+#+     +:+    +#+    +#++:++#+ +#++:++#  +#++:++#:    
+#+   +#+     +#+    +#+       +#+       +#+    +#+    
#+#+#+#      #+#    #+#       #+#       #+#    #+#     
 ###    ##############       #############    ###      
         
\033[1;91m
##      ## ######## ########   ######   ######     ###    ##    ## ##    ## ######## ########  
##  ##  ## ##       ##     ## ##    ## ##    ##   ## ##   ###   ## ###   ## ##       ##     ## 
##  ##  ## ##       ##     ## ##       ##        ##   ##  ####  ## ####  ## ##       ##     ## 
##  ##  ## ######   ########   ######  ##       ##     ## ## ## ## ## ## ## ######   ########  
##  ##  ## ##       ##     ##       ## ##       ######### ##  #### ##  #### ##       ##   ##   
##  ##  ## ##       ##     ## ##    ## ##    ## ##     ## ##   ### ##   ### ##       ##    ##  
 ###  ###  ######## ########   ######   ######  ##     ## ##    ## ##    ## ######## ##     ## 


''')
	print (l)
def start(url,cookie,timeo,date,head=None):
	global rfile,no
	if nopar:
		headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	elif yeh:
		v.sqli(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.xss(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.osinj(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.ssti(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	else:
		v.sqli(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.xss(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.osinj(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		v.ssti(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
def start_header(url,cookie,timeo,date,head=None):
	headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
def threader():
	while True:
		item = q.get()
		start(item,cookie,timeo,date)
		q.task_done()
def threader2():
	while True:
		item = w.get()
		start_header(item,cookie,timeo,date)
		w.task_done()
if __name__ == "__main__":
	try:
		logo()
		v=paramscanner()
		getargs()
		if modulee == True:
			try:
				run = module.script()
				if d['list_support'] == True:
					if rfile:
						try:
							f = open(rfile,'r')
						except:
							logger.error('File Error')
							exit()
						the_options['file'] = f
						run.run(the_options)
				else:
					run.run(the_options)
			except:
				logger.critical(f'Module Error ({red}Code{end})')
				exit()
		if url:
			con(url,vert=vert,redir=redir,cookie=cookie,timeo=timeo,proxy=proxy,slp=sleep,cagent=cagent)
		if r:
			try:
				rfile=open(rfile,'r')
			except FileNotFoundError:
				print(f"{bad} File Not Found..!")
				exit()
			q = Queue()
			w = Queue()
			for i in range(thr):
				if nopar:
					t2 = threading.Thread(target=threader2)
					t2.daemon = True
					t2.start()
				elif yeh:
					t1 = threading.Thread(target=threader)
					t1.daemon = True
					t1.start()
				else:
					t1 = threading.Thread(target=threader)
					t1.daemon = True
					t2 = threading.Thread(target=threader2)
					t2.daemon = True
					t1.start()
					t2.start()
			for url in rfile:
				url=url.replace('<','').replace('>','').replace('{','').replace('}','').replace("<%","").replace("%>","").replace("'","").replace('"',"").replace("|",'').strip()
				if url.startswith('http://') or url.startswith('https://'):
					no = False
				else:
					no = False
					url='http://'+url
				wh=con_f(url,vert=vert,proxy=proxy,redir=redir,cookie=cookie,timeo=timeo,slp=sleep,cagent=cagent)
				if wh == 'ok':
					if '?' in url or '*' in url:
						no = False
					else:
						if nopar:
							w.put(url)
						print(f"{bad} No parameters :v")
						no = True
					if no == False:
						q.put(url)
				elif wh[0] == 'no':
					print(f"\n{bad} {wh[1]}")
			if nopar:
				w.join()
			if yeh:
				q.join()
			exit()
		if r == True or date != None:
			pass
		else:
			if url.startswith('http://') or url.startswith('https://'):
				pass
			else:
				url='http://'+url
			if '?' in url or '*' in url or date != None:
				pass
			else:
				if yeh:
					print(f"{bad} Please Add parameters or (*) in url ")
					exit()
				headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				print(f"{bad} Please Add parameters or (*) in url ")
				exit()
		if date:
			if nopar:
				headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
			elif yeh:
				v.xss_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.sqli_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.osinj_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.ssti_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
			else:
				v.xss_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.sqli_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.osinj_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.ssti_post(url,cookie,timeo,date,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_ssti(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,date=date,method='post',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
		else:
			if nopar:
				headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
			elif yeh:
				v.sqli(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.xss(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.osinj(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.ssti(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
			else:
				v.sqli(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.xss(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.osinj(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				v.ssti(url,cookie,timeo,encoded,vert,redir,cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.referrer_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_xss(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_sqli(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
				headers_scanner.user_agent_rce(url,cookie=cookie,timeo=timeo,deco=encoded,vert=vert,redir=redir,method='get',cagent=cagent,proxy=proxy,slp=sleep,batch=batch)
	except KeyboardInterrupt:
		print(f'\n{bad} Good Bye :)\n')
		exit()
	except RuntimeError:
		logger.error(f"\n{bad} can't start new thread .. ('--threads=100')")
		exit()
	except requests.exceptions.ConnectionError:
		logger.error(f"host '{blue}{url}{end}' does not exist ..!")
		exit()
	except requests.exceptions.ReadTimeout:
		logger.error(f"\nTimeout Error ")
		exit()
	except requests.exceptions.ProxyError:
		logger.error(f"Proxy Connection Error")
		exit()
	except requests.exceptions.InvalidURL:
		logger.error(f"Invalid URL")
		exit()
	except requests.exceptions.InvalidSchema:
		logger.error(f"Invalid Schame")
		exit()
	except requests.exceptions.MissingSchema:
		logger.error(f"Missing Schema")
		exit()