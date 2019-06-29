#@Author: Bilal CAN

import csv
import os

dev_dict ={}
with open('Results/arranged_collected_data.csv', 'r') as arranged_data:
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
            if key2 == '2013': continue
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
                     '2011':0,
                     '2012':0},
                    1
                    ]
                (dev_dict[key1])[0][key2] += 1
                
dev_num = len(dev_dict)
work_num = count_line

with open('Results/arranged_dev_num.csv', 'w', newline='') as toWrite:
    writer = csv.writer(toWrite, delimiter='\t')
    writer.writerow(('developer', '2006', '2007', '2008', '2009', '2010', '2011', '2012', 'total'))
    for key in dev_dict:
        writer.writerow((key,
                         dev_dict[key][0]['2006'],
                         dev_dict[key][0]['2007'],
                         dev_dict[key][0]['2008'],
                         dev_dict[key][0]['2009'],
                         dev_dict[key][0]['2010'],
                         dev_dict[key][0]['2011'],
                         dev_dict[key][0]['2012'],
                         dev_dict[key1][1]))

lower10 = {}; lower25 = {}; lower50 = {}; lower75 = {};
lower100 = {}; lower150 = {}; lower200 = {}; lower250 = {};
higher250 = {}
for key in dev_dict:
    if dev_dict[key][1] <= 10: lower10.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 25: lower25.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 50: lower50.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 75: lower75.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 100: lower100.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 150: lower150.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 200: lower200.update({key: dev_dict[key]})
    elif dev_dict[key][1] <= 250: lower250.update({key: dev_dict[key]})
    else: higher250.update({key: dev_dict[key]})

criteria1 = {}
criteria2 = {}
criteria3 = {}
for key in dev_dict:
    if (dev_dict[key][0]['2011'] != 0) or (dev_dict[key][0]['2012'] != 0):
        if (key in lower250) or (key in higher250):
            criteria1.update({key: dev_dict[key]})
for key in dev_dict:
    if (dev_dict[key][0]['2012'] != 0):
        if (key in lower250) or (key in higher250):
            criteria2.update({key: dev_dict[key]})
for key in dev_dict:
    if (dev_dict[key][0]['2012'] >= 10):
        if (key in lower250) or (key in higher250):
            criteria3.update({key: dev_dict[key]})
with open('Results/arranged_histogram.txt', 'w') as histogram:
    print("""The number of developers: %d
The total number of works: %d
Developers according to works:
up to 10: %d
11-25   : %d
26-50   : %d
50-75   : %d
75-100  : %d
100-150 : %d
150-200 : %d
200-250 : %d
250+    : %d
Criteria 1 : %d
Criteria 2 : %d
Criteria 3 : %d"""%(dev_num,
                    work_num,
                    len(lower10),
                    len(lower25),
                    len(lower50),
                    len(lower75),
                    len(lower100),
                    len(lower150),
                    len(lower200),
                    len(lower250),
                    len(higher250),
                    len(criteria1),
                    len(criteria2),
                    len(criteria3)), flush=True, file=histogram)
    
#CRITERIA 2 is chosen"
if not os.path.exists('General'):
    os.makedirs('General')
rewrite = open('General/mozilla_learning_data.csv', 'w', newline = '')
writer = csv.writer(rewrite, delimiter = '\t')
writer.writerow(('id', 'time', 'developer', 'short_desc'))
with open('Results/arranged_collected_data.csv', 'r') as arranged_data:
    reader = csv.reader(arranged_data, delimiter = '\t')
    count_line = 0
    for row in reader:
        if count_line == 0:
            count_line += 1
            continue
        else:
            if row[2] in criteria2:
                writer.writerow((row[0], row[1], row[2], row[3]))
rewrite.close()
