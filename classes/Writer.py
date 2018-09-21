'''
Created on 2018/09/16

@author: Kusunoki
'''
import csv

def Txt(file_path, written_text):
    with file_path('text.txt', 'w') as f:
        f.write(written_text)
        
        
def OutputCsv(file_path, array2d, line_char = "\n" , delimit_char = ","):
    with open('some.csv', 'w') as f:
        writer = csv.writer(f, lineterminator=line_char, delimitter = delimit_char) # 改行コード（\n）を指定しておく
        writer.writerow(list)     # list（1次元配列）の場合
        writer.writerows(array2d) # 2次元配列も書き込める