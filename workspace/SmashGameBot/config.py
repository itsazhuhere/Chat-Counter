'''
Created on Dec 24, 2016

@author: Andre
'''
import pymysql.cursors

connect_dict = dict(host="localhost",
                    user='root',
                    password='no1knows',
                    db='smashgames',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)