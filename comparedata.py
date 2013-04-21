# -*- coding: utf-8 -*-
import dealcsv
import difflib

hasproc_count = 0 
totalcount =  0

#需要过滤掉的字符内容
filtercontent = ()

def comparedata(data1,data2,firstcolumns,secondcolumns,firstincludecolumns=None,secondincludecolumns=None,needratio=0,mini_ratio_percent=1.0):
    """
    compare two directory with special keys
    @data1 directory
    @data2 directory
    @columns list ,special key names 
    @includecolumns should include in result ,like [('b'),('b')]
    """
    global totalcount
    global hasproc_count
    totalcount = len(data1) * len(data2)
    print "comparedata.totalcount=%s"%totalcount
    if (not firstcolumns or len(firstcolumns)<=0) or (not secondcolumns or len(secondcolumns)<=0) :
        raise Exception("please special comparing columns")
    firstcolumn =  firstcolumns[0]
    secondcolumn = secondcolumns[0]
   
    
    if not data1[0].has_key(firstcolumn):
        raise Exception("data1don't have special column %s"%firstcolumn)
    #print data2
    if not data2[0].has_key(secondcolumn):
        raise Exception("data2 don't have special column %s"%secondcolumn)
    
    result = []

    for first_row in data1:
        firstval = first_row[firstcolumn]
        for second_row in data2:
            result_row = _createrow(first_row,second_row,firstcolumn,secondcolumn,firstincludecolumns,secondincludecolumns,needratio,mini_ratio_percent)
            if result_row:
                result.append(result_row)
                break
        hasproc_count = hasproc_count + len(data2)
        #print "comparedata.hasproc_count=%s"%hasproc_count
    return result


def _createrow(first_row,second_row, firstcolumn,secondcolumn,firstincludecolumns=None,secondincludecolumns=None,needratio=0,mini_ratio_percent=1.0):
    """
    generate one result row
    @first_row          first row 
    @second_row         second row
    @firstcolumn        column names
    @includecolumns     all columns which should be included in result 
    """
    firstval = str(first_row[firstcolumn])
    secondval = str(second_row[secondcolumn])
    firstval = firstval and firstval.strip()
    secondval = secondval and secondval.strip()
	
    if not firstval or not secondval:
	return None
    
    global filtercontent
    print  filtercontent

    if filtercontent:
        for field in filtercontent:
            if field in firstval:
                firstval = firstval.replace(field,"")
            if field in secondval:
                secondval = secondval.replace(field,"")

    compare_result = False
    s_ratio = 0
    if needratio:
        s = difflib.SequenceMatcher(None,firstval,secondval) 
        s_ratio = s.ratio()
        if s_ratio<mini_ratio_percent:
            #print "%s and %s similar = %s" % str(s_ratio)
            #return None
            compare_result = False
        else:
            compare_result = True
    else:
        if firstval<> secondval:
            return None
        else:
            compare_result = True
    
    if not compare_result:
        return None

    result = {}
    
    if needratio:
        result["compare similar percent"] = s_ratio

    result['data1_%s'%firstcolumn] = firstval

    if firstincludecolumns:
        for item in firstincludecolumns:            
            result['data1_%s'%item] = first_row[item]
        
    result['data2_%s'%secondcolumn] = second_row[secondcolumn]

    if secondincludecolumns:    
        for item in secondincludecolumns:
            result['data2_%s'%item] = second_row[item]
    return result


def comparecsv(firstfile,secondfile,firstcolumns,secondcolumns,firstincludecolumns=None,secondincludecolumns=None,determiter=',',needratio=0,mini_ratio_percent=1.0):
    """
    @purpose        Compare two csv file
    @firstfile      first csv file
    @secondfile     second csv file
    @columns        compare columns
    @determiter     sepater character
    @includecolumns should be included in result
    @reutrn [{},{}]
    """
    data1 = dealcsv.get_content_with_directory(firstfile,determiter)
    data2 = dealcsv.get_content_with_directory(secondfile,determiter)
    return comparedata(data1,data2,firstcolumns,secondcolumns,firstincludecolumns,secondincludecolumns,needratio=needratio,
                       mini_ratio_percent=mini_ratio_percent)


#from filter.csv loading filter fields 
import os
if os.path.exists("filter.csv"):
    with open("filter.csv","rb") as csvfile:
        #global filtercontent
        filtercontent = tuple(csvfile.readlines())
        
if __name__ =="__main__":
    d1 = [{'a':"123",'b':2},{'a':23,'b':45}]
    d2 = [{'a':"13",'b':23},{'a':4,'b':45},{'a':23,'b':45}]
    #filtercontent = ('2',)
    print filtercontent
    result = comparedata(d1,d2,['a'],['a'],['b'],['b'],needratio=1,mini_ratio_percent=0.8)
    print result
