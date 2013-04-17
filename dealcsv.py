# -*- coding: utf-8 -*-

import csv
import os.path

def get_headers(filepath,determiter=','):
    if not filepath or not os.path.exists(filepath):
        raise IOError("file %s not found "%filepath)
    with open(filepath,'rb') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        return header

def get_content_with_directory(filepath,determiter=','):
    header = get_headers(filepath,determiter)
    result = []
    with open(filepath,'rb') as csvfile:
        datas = csv.reader(csvfile)
        datas.next() #remove header
        for row in datas:
            temp={}
            items = zip(header,row)
            for (name,value) in items:
                temp[name] = value
            result.append(temp)
    return result

if __name__ =="__main__":
    header = get_headers("demodata.csv")
    print "demodata is %s " % (len(header)>0)
    try:
        header = get_headers("nofile.csv")
    except IOError:
        print 'file nofile is not exists'

    result = get_content_with_directory("demodata.csv")
    print result.keys()
    print result.values()
