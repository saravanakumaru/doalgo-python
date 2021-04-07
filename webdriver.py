# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from kiteconnect import KiteConnect 

import time
import os

browser = webdriver.Chrome(executable_path='/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/chromedriver')
browser.get('https://www.google.com/')

        