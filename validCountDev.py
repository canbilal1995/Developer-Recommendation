#@Author: Bilal CAN

import csv

dev_dict ={}
with open('Results/arranged_data.csv', 'r') as arranged_data:
    reader = csv.reader(arranged_data, delimiter = '\t')
    count_line = 0
    for row in reader:
        if count_line == 0:
            count_line += 1
            continue
        else:
            count_line += 1
            key1 = row[2]
            key2 = (row[1])[:4]
            if key1 in dev_dict:
                (dev_dict[key1])[0][key2] += 1
                (dev_dict[key1])[1] += 1
            else:
                dev_dict[key1] = [
                    {'2006':0,
                     '2007':0,
                     '2008':0,
                     '2009':0,
                     '2010':0,
                     '2011':0},
                    1
                    ]
                (dev_dict[key1])[0][key2] += 1

with open('Results/arranged_dev_num.csv', 'w', newline='') as toWrite:
    writer = csv.writer(toWrite, delimiter='\t')
    writer.writerow(('developer', '2006', '2007', '2008', '2009', '2010', '2011'))
    for key in dev_dict:
        writer.writerow((key,
                         dev_dict[key][0]['2006'],
                         dev_dict[key][0]['2007'],
                         dev_dict[key][0]['2008'],
                         dev_dict[key][0]['2009'],
                         dev_dict[key][0]['2010'],
                         dev_dict[key][0]['2011']))
