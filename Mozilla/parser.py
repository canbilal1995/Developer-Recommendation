#@Author: Bilal CAN

from xml.etree import ElementTree as ET
import csv
import os
import datetime

with open('Resources/bugzilla_assigned_to.xml','rt') as bugzilla_dev:
    bugzilla_dev_tree = ET.parse(bugzilla_dev)
with open('Resources/bugzilla_resolution.xml','rt') as bugzilla_res:
    bugzilla_res_tree = ET.parse(bugzilla_res)
with open('Resources/bugzilla_short_desc.xml','rt') as bugzilla_desc:
    bugzilla_desc_tree = ET.parse(bugzilla_desc)

with open('Resources/core_assigned_to.xml','rt') as core_dev:
    core_dev_tree = ET.parse(core_dev)
with open('Resources/core_resolution.xml','rt') as core_res:
    core_res_tree = ET.parse(core_res)
with open('Resources/core_short_desc.xml','rt') as core_desc:
    core_desc_tree = ET.parse(core_desc)

with open('Resources/firefox_assigned_to.xml','rt') as firefox_dev:
    firefox_dev_tree = ET.parse(firefox_dev)
with open('Resources/firefox_resolution.xml','rt') as firefox_res:
    firefox_res_tree = ET.parse(firefox_res)
with open('Resources/firefox_short_desc.xml','rt') as firefox_desc:
    firefox_desc_tree = ET.parse(firefox_desc)

with open('Resources/thunderbird_assigned_to.xml','rt') as thunderbird_dev:
    thunderbird_dev_tree = ET.parse(thunderbird_dev)
with open('Resources/thunderbird_resolution.xml','rt') as thunderbird_res:
    thunderbird_res_tree = ET.parse(thunderbird_res)
with open('Resources/thunderbird_short_desc.xml','rt') as thunderbird_desc:
    thunderbird_desc_tree = ET.parse(thunderbird_desc)

all_id = {}
all_dev = {}
all_desc = {}
res_tree = [bugzilla_res_tree, core_res_tree, firefox_res_tree, thunderbird_res_tree]
dev_tree = [bugzilla_dev_tree, core_dev_tree, firefox_dev_tree, thunderbird_dev_tree]
desc_tree = [bugzilla_desc_tree, core_desc_tree, firefox_desc_tree, thunderbird_desc_tree]
all_id01 = {}
all_dev01 = {}
all_desc01 = {}

for traverser in range(4):
    for node in res_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        for child in node.findall('.//update'):
            if(child[1].text == 'FIXED' or child[1].text == 'WORKSFORME'):
                all_id01.update({report_id : child[0].text})
                break

    for node in dev_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        if report_id in all_id01:
            i = 0;
            for child in node.findall('.//update/what'):
                if i == 1 :
                    all_dev01.update({report_id : child.text})
                i += 1
    for node in desc_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        for i in range(len(all_dev01)):
            if report_id in all_dev01:
                child = node.find('.//update/what')
                all_desc01.update({report_id : child.text})
                break
    all_dev.update(all_dev01)
    all_id.update(all_id01)
    all_desc.update(all_desc01)
    all_id01.clear()
    all_dev01.clear()
    all_desc01.clear()
    
print('Developers:', len(all_dev))
print('All reports valid:', len(all_id))
print('Matched reports short desc:', len(all_desc))

if not os.path.exists('Results'):
    os.makedirs('Results')
toWrite = []
with open('Results/collected_data.csv', 'w', newline='') as collected_data:
    writer = csv.writer(collected_data, delimiter = '\t')
    writer.writerow(('id', 'time', 'developer', 'short_desc'))
    for key_id in all_dev:
        try:
            date = datetime.datetime.fromtimestamp(int(all_id[key_id])).strftime('%Y-%m-%d %H:%M:%S')
            toWrite.append((key_id, date, all_dev[key_id], all_desc[key_id]))
        except:
            continue
    toWrite.sort(key = lambda a : a[2])#According to developers since I want to see easily developers' active years
    for row in toWrite:
        try:
            if 'inbox' in row[2]: continue
            writer.writerow((row[0], row[1], row[2], row[3]))
        except:
            continue
print('All data is written to the csv file.')
