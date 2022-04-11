


'''
Function which takes a matrix of text found in the page, and converts it into a useful table

'''
from matplotlib.pyplot import text


textArrays = [['ARCO', 'LIMITED', 'SUBSIDIARIES'], ['CONSOLIDATED', 'INCOME', 'STATEMENT', 'FOR', 'THE', 'YEAR', 'ENDED', '2021'], ['2021', '2020'], ['Note', "£'000", '£000'], ['Turnover', '390,21', '9,968'], ['Cost', 'Sales', '(309,548)', '(244,536)'], ['Gross', 'Profit', '80,671', '75,432'], ['Distribution', 'costs', '(30,526)', '(32,777)'], ['Administrative', 'expenses', '(31', ',669)', '(31', ',924)'], ['Exceptional', 'income'], ['Operating', 'Profit', '8,887', '10,731'], ['(Loss)', 'profit', 'disposal', 'tangible', 'asset(s)', '(287)', '2,888'], ['Profit', 'Before', 'Interest', 'and', 'Taxation', '8,600', '3,61'], ['Interest', 'receivable', 'and', 'similar', 'income'], ['Interest', 'payable', 'and', 'similar', 'expenses', '(330)', '(582)'], ['Profit', 'Before', 'Taxation', '8,299', '13,095'], ['Tax', 'profit', '9a,9c', '(4,306)', '(1,630)'], ['Profit', 'for', 
'the', 'financial', 'year', '13,993', '11,465'], ['CONSOLIDATED', 'STATEMENT', 'COMPREHENSIVE', 'INCOME'], ['FOR', 'THE', 'YEAR', 'ENDED', 'JUNE', '2021'], ['Note', '2021', '2020'], ['£’000', '£’000'], ['Profit', 'for the financial', 'year', '13,993', '11,465'], ['Other', 'comprehensive', 'income', '(expense)'], ['Remeasurement', 'net', 'defined', 'benefit', 'obligation', '14,274'], ['Deferred', 'tax', 'on-defined', 'benefit', 'obligation', '(3,569)', '224'], ['Tax', 'rate', 'change', 'movement', 'deferred', 'tax'], ['‘relating', 'revaluation', 'pension', 'deficit', '543'], ['rate', 'change', 'movement', 'derivatives'], ['Purchase', 'own', 'shares'], ['Current', 'year', 'deferred', 'tax', 'corporation', 'tax', 
'rate', '(433)'], ['Cash', 'flow', 'hedges', '140'], ['Deferred', 'tax', 'cash', 'flow', 'hedge', '(63)', '(27)'], ['Currency', 'movement', 'overseas', 'investments', '148'], ['Other', 'comprehensive', 'income', '(expense)', 'for'], ['the', 'year,', 'net', 'tax', ',986', '(261'], ['Total', 'comprehensive', 'income', 'for', 'the', 'year', '25,979', '11,204']]

numColumns=3
columnHeaders=['label','y0','y1']

dict={}

for columnNum in range(numColumns):
    columndata=[]
    for row in textArrays:
        print(row)
        try:
            columndata.append(row[columnNum])
        except(IndexError):
            pass
    print(columnNum)
    print(columnHeaders[columnNum])
    dict[columnHeaders[columnNum]]=[columndata]

print(dict)


def dataToTable(textArrays,numColumns=3,columnHeaders=['label','y0','y1']):
    print('Converting text found to table')


    dict = {"Name":[],"Address":[],"Age":[]}

    dict["Age"].append(30)
    print(dict)
    
        

