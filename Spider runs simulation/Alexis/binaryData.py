setwd("~/Downloads")

import csv
#csvfilename = '/Users/alexispark/Downloads/Metazygia wittfeldae Monitor 1 activity_DD.csv'
csvfilename = 'Metazygia wittfeldae Monitor 1 activity_DD.csv'

def read_csvfile(filename):
    count = 0
    data = []
    with open(filename) as f:
        for line in f:
            if count == 0:
                fields = line.rstrip().split(',')
            else:
                items = line.rstrip().split(',')
                for i, val in enumerate(items):
                    if i >= 2 and int(val) > 0:
                        items[i] = '1'
                data.append(items)
            count += 1
    return(fields,data)

(fields,rows) = read_csvfile(csvfilename)
newfilename = "DD_Monitor_1_activity_binary.csv"
# writing to csv file 
with open(newfilename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    csvwriter.writerow(fields) 
        
    csvwriter.writerows(rows)

