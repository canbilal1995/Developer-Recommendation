#@Author: Bilal CAN

import csv

dev_dict ={}
with open('Results/collected_data.csv', 'r') as collected_data:
    reader = csv.reader(collected_data, delimiter = '\t')
    count_line = 0
    for row in reader:
        if count_line == 0:
            count_line += 1
            continue
        else:
            count_line += 1
            key = row[1]
            if key in dev_dict:
                dev_dict[key] += 1
            else:
                dev_dict[key] = 1
work_num = 0
dev_num = 0
lower10 = {}
lower25 = {}
lower50 = {}
lower100 = {}
lower250 = {}
higher250 = {}
for key in dev_dict:
    work_num += dev_dict[key]
    dev_num += 1
    if dev_dict[key] <= 10: lower10.update({key : dev_dict[key]})
    elif dev_dict[key] <= 25: lower25.update({key : dev_dict[key]})
    elif dev_dict[key] <= 50: lower50.update({key : dev_dict[key]})
    elif dev_dict[key] <= 100: lower100.update({key : dev_dict[key]})
    elif dev_dict[key] <= 250: lower250.update({key : dev_dict[key]})
    else: higher250.update({key : dev_dict[key]})

print("Total number of work: %d"%work_num)
print(f'Total number of developers: {dev_num}')
print("""Dev Numbers according to works:
up to 10: %d
11-25   : %d
26-50   : %d
51-100  : %d
101-250 : %d
251+    : %d
"""%(len(lower10),len(lower25),len(lower50),len(lower100),len(lower250),len(higher250)))

with open('Results/developer_number.csv', 'w', newline='') as dev_num_csv:
    fieldnames = ['developers', 'number of work']
    writer = csv.writer(dev_num_csv, delimiter='\t')
    writer.writerow(fieldnames)
    for key in dev_dict:
        writer.writerow((key, dev_dict[key]))
