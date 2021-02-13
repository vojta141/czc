import requests
from selenium import webdriver

from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

codeDriver = webdriver.Firefox()
codeDriver.get('https://www.czc.cz/premiumcord-redukce-stereojack-2-5mm-3-5mm-m-f/62917/produkt')
sleep(5)
s = requests.Session()
s.get('https://www.czc.cz')
data = {'callCount':'1',
'c0-scriptName':'__System',
'c0-methodName':'generateId',
'c0-id':'0',
'batchId':'0',
'instanceId':'0',
'page':'%2F',
'scriptSessionId':''}
response = s.post('https://www.czc.cz/dwr/call/plaincall/__System.generateId.dwr', data=data)
DWRSESSION = str(response.text.split('dwr.engine.remote.handleCallback("0","0","')[1].split('\n')[0][:-3])
s.cookies.update({'DWRSESSIONID':DWRSESSION})
print(s.cookies)


def getSessionId(dwrsession):
    second = codeDriver.execute_script('return dwr.engine.util.tokenify(new Date().getTime()) + "-" + dwr.engine.util.tokenify(Math.random() * 1E16);')
    return dwrsession + '/' + second



