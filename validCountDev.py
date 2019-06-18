#@Author: Bilal CAN

import csv
import matplotlib.pylab as plt

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
