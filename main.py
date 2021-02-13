
import datetime
from time import sleep

import requests
from lxml import html

import json

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

s = requests.Session()
s.get('https://www.czc.cz')

count = 0
bought = open('codes.txt', 'w')
linksBought = []
url = 'https://www.czc.cz/herni-graficke-karty/produkty?q-c-3-f_2027483=sGeForce%20GTX%201660&q-c-7-f_2027483=sGeForce%20GTX%201650%20Super&q-c-8-f_2027483=sGeForce%20RTX%203060&q-c-4-f_2027483=sGeForce%20GTX%201660%20Super&q-c-0-f_2027483=sGeForce%20RTX%203060%20Ti&q-c-6-f_2027483=sRadeon%20RX%205500%20XT&q-c-9-f_2027483=sRadeon%20RX%205600%20XT&q-c-1-f_2027483=sGeForce%20RTX%203070&q-c-5-f_2027483=sGeForce%20GTX%201660%20Ti&q-c-2-f_2027483=sGeForce%20RTX%203080&q-first='
print('Running')
iter = 0
while True:
        for i in range(0, 6):
            s = requests.Session()
            response = s.get(url + str(i*27))
            tree = html.fromstring(response.content)
            f = open('cards.html', 'w')
            f.write(response.text)
            f.close()
            items = tree.xpath('//*[@class="new-tile"]')
            for item in items:
                stock = item.find_class('availability-state-on-stock')
                link = item.find_class('image')[0].attrib.get('href')

                if len(stock) != 0:
                    if link not in linksBought:
                        print(link)
                        linksBought.append(link)
                        name = json.loads(item.attrib.get('data-ga-impression'))['name']
                        log = open('log.txt', 'a')
                        log.write(name + '    ' + str(datetime.datetime.now()) + '\n')
                        log.close()
                        print('CARD IN STOCK: ' + name)
                        link = item.find_class('lazy-load lazy-loaded')
                        driver = webdriver.Firefox()
                        driver.get('https://www.czc.cz' + str(link))
                        driver.find_element_by_xpath('//*[@class="btn btn-buy"]').click()
                        driver.get('https://www.czc.cz/kosik/dodaci-udaje')
                        driver.find_element_by_xpath('//*[@class="btn keep_basket js-login"]').click()
                        driver.find_element_by_id('frm-registration.email').send_keys('vojtadtenis@gmail.com')
                        driver.find_element_by_id('frm-registration.phoneNumberFormatted').send_keys('704057325')
                        driver.find_element_by_id('frm-registration.name').send_keys('Vojtěch')
                        driver.find_element_by_id('frm-registration.surname').send_keys('Drška')
                        driver.find_element_by_id('frm-registration.street').send_keys('Hradební 508')
                        driver.find_element_by_id('frm-registration.city').send_keys('Nymburk')
                        driver.find_element_by_id('frm-registration.zipCodeFormatted').send_keys('28802')
                        try:
                            driver.find_element_by_xpath('//*[@class="btn btn-purchase"]').click()
                        except:
                            driver.find_element_by_xpath('//*[@class="popup-close close btn-remove"]').click()
                            sleep(4)
                            driver.find_element_by_xpath('//*[@class="btn btn-purchase"]').click()
                        sleep(1)
                        driver.implicitly_wait(5)
                        driver.find_element_by_xpath('//*[@class="btn btn-purchase"]').click()

        sleep(0.7)
        iter += 1
        if(iter >= 30):
            print('STATUS: OK' + ' ' + str(datetime.datetime.now()))
            iter = 0
