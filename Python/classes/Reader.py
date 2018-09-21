'''
Created on 2018/09/16

@author: Kusunoki
'''
import csv

def Csv(file_path):
    text_lines = [];
    with open('test.txt','r') as f:
        for row in f:
            print row.strip()
    return text_lines



    