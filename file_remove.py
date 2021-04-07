#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 20:57:07 2021

@author: saravana.kumar
"""

import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")
import time
import os

from kiteconnect import KiteConnect
from selenium import webdriver



cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

if os.path.exists("token_created.txt"):
    os.remove("token_created.txt")
    print("File Deleted.... ")