
def comparedata(data1,data2,columns,includecolumns):
    """
    compare two directory with special keys
    @data1 directory
    @data2 directory
    @columns list ,special key names 
    @includecolumns should include in result ,like [('b'),('b')]
    """
    if not columns or len(columns)<=0:
        raise Exception("please special comparing columns")
    firstcolumn = columns[0]
    if not data1[0].has_key(firstcolumn) and not data2[0].has_key(firstcolumn):
        raise Exception("data1 or data2 don't have special column %s"%firstcolumn)
    
    result = []

    for first_row in data1:
        firstval = first_row[firstcolumn]
        for second_row in data2:
            #secondval = second_row[firstcolumn]
            #if firstval == secondval:
            #    result.append({'data1_%s'%firstcolumn:firstval,'data2_%s'%firstcolumn:secondval})
            result_row = _createrow(first_row,second_row,firstcolumn,includecolumns)
            if result_row:
                result.append(result_row)
                break
    return result

def _createrow(first_row,second_row, firstcolumn,includecolumns):
    """
    generate one result row
    @first_row          first row 
    @second_row         second row
    @firstcolumn        column names
    @includecolumns     all columns which should be included in result 
    """
    firstval = str(first_row[firstcolumn])
    secondval = str(second_row[firstcolumn])
    firstval = firstval and firstval.strip()
    secondval = secondval and secondval.strip()

    if firstval<> secondval:
        return None

    result = {}
    result['data1_%s'%firstcolumn] = first_row[firstcolumn]

    for item in includecolumns[0]:
        result['data1_%s'%item] = first_row[item]
    result['data2_%s'%firstcolumn] = second_row[firstcolumn]
        
    for item in includecolumns[0]:
        result['data2_%s'%item] = second_row[item]

    return result


if __name__ =="__main__":
    d1 = [{'a':1,'b':2},{'a':23,'b':45}]
    d2 = [{'a':1,'b':23},{'a':4,'b':45},{'a':23,'b':45}]
    result = comparedata(d1,d2,['a'],[('b',),('b',)])
    print result
