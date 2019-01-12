#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ConfigParser import SafeConfigParser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

CONFIG_PATH = './strava.config'
STRAVA = 'STRAVA'

class StravaKudos:
  def __init__(self):
    self.config = SafeConfigParser()
    self.config.read(CONFIG_PATH)

    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('start-maximized') # 
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    chromedriver = self.config.get(STRAVA, 'chromedriver')
    if not chromedriver:
      print 'Please provide the correct path to chromedriver in strava.config file'
      sys.exit(1)

    os.environ["webdriver.chrome.driver"] = chromedriver
    self.driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

  def login(self):
    login = self.config.get(STRAVA, 'email')  
    if not login:
      print 'Please provide your strava login in strava.config file'
      sys.exit(1)

    password = self.config.get(STRAVA, 'password')  
    if not password:
      print 'Please provide your strava password in strava.config file'
      sys.exit(1)

    self.driver.get('https://www.strava.com/login')  
    self.driver.find_element_by_id('email').send_keys(login)
    self.driver.find_element_by_id ('password').send_keys(password)
    self.driver.find_element_by_id('login-button').click()

  def giveKudos(self, num):    
    self.driver.get('https://www.strava.com/dashboard/following/' + num)
    cnt = 0  
    for element in self.driver.find_elements_by_css_selector('button.js-add-kudo'):
      self.driver.execute_script('arguments[0].click();', element)
      cnt += 1
    print 'Gave ' + str(cnt) + '/' + num + ' kudos '   

def createConfigFile():
  f = open(CONFIG_PATH, "w+")   
  f.write('[' + STRAVA+']\n')
  f.write('email = your_strava@email.com\n')
  f.write('password = your_strava_password\n')
  f.write('chromedriver = path_to_chromedriver\n\n')
  f.write('# chromedriver can be downloaded from: http://chromedriver.chromium.org/downloads\n')
  f.close()  

def main():
  args = sys.argv[1:]
  if not args:
    print 'usage: ./strava.py activities_number'
    sys.exit(1)

  if not os.path.exists(CONFIG_PATH):
    print 'Please update config file: ' + CONFIG_PATH 
    createConfigFile()
    sys.exit(1)
  
  kudos = StravaKudos()
  kudos.login()
  kudos.giveKudos(args[0])  
  
if __name__ == '__main__':
  main()
