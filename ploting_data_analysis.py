#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:31:50 2021

@author: saravana.kumar
this file is to practice the ploting functionality of python
"""
import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")
import pandas as pd 
import os
import seaborn as sb

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")
data = pd.read_csv("data-nse.csv",parse_dates=['Date']) 
data.set_index('Date')
data['percentage_increase'] = data['Close'] / data['Open']
data['day'] = data['Date'].apply(lambda x : x.strftime('%A'))
data_green_days= data[data['percentage_increase'] > 1.0]
data_green_days_group_by = data_green_days.groupby(['day']).count()
data_green_days_group_by.reset_index(inplace=True)
ax = sb.histplot(data=data_green_days,x='day')
# sb.barplot(data=data_green_days_group_by,x='day',y='Date');
ax.set(ylim=(5, 40))
