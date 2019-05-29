#@Author: Bilal CAN

from xml.etree import ElementTree as ET
import csv
import os
import datetime
import operator

with open('Resources/cdt_assigned_to.xml','rt') as cdt_dev:
    cdt_dev_tree = ET.parse(cdt_dev)
with open('Resources/jdt_assigned_to.xml','rt') as jdt_dev:
    jdt_dev_tree = ET.parse(jdt_dev)
with open('Resources/pde_assigned_to.xml','rt') as pde_dev:
    pde_dev_tree = ET.parse(pde_dev)
with open('Resources/cdt_resolution.xml','rt') as cdt_res:
    cdt_res_tree = ET.parse(cdt_res)
with open('Resources/jdt_resolution.xml','rt') as jdt_res:
    jdt_res_tree = ET.parse(jdt_res)
with open('Resources/pde_resolution.xml','rt') as pde_res:
    pde_res_tree = ET.parse(pde_res)
with open('Resources/cdt_bug_status.xml','rt') as cdt_bug:
    cdt_bug_tree = ET.parse(cdt_bug)
with open('Resources/jdt_bug_status.xml','rt') as jdt_bug:
    jdt_bug_tree = ET.parse(jdt_bug)
with open('Resources/pde_bug_status.xml','rt') as pde_bug:
    pde_bug_tree = ET.parse(pde_bug)
with open('Resources/cdt_short_desc.xml','rt') as cdt_desc:
    cdt_desc_tree = ET.parse(cdt_desc)
with open('Resources/jdt_short_desc.xml','rt') as jdt_desc:
    jdt_desc_tree = ET.parse(jdt_desc)
with open('Resources/pde_short_desc.xml','rt') as pde_desc:
    pde_desc_tree = ET.parse(pde_desc)
with open('Resources/platform_assigned_to.xml','rt') as platform_dev:
    platform_dev_tree = ET.parse(platform_dev)
with open('Resources/platform_resolution.xml','rt') as platform_res:
    platform_res_tree = ET.parse(platform_res)
with open('Resources/platform_bug_status.xml','rt') as platform_bug:
    platform_bug_tree = ET.parse(platform_bug)
with open('Resources/platform_short_desc.xml','rt') as platform_desc:
    platform_desc_tree = ET.parse(platform_desc)
    
all_id = {}
all_dev = {}
all_desc = {}
res_tree = [cdt_res_tree, jdt_res_tree, pde_res_tree, platform_res_tree]
dev_tree = [cdt_dev_tree, jdt_dev_tree, pde_dev_tree, platform_dev_tree]
desc_tree = [cdt_desc_tree, jdt_desc_tree, pde_desc_tree, platform_desc_tree]
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
    toWrite.sort(key = operator.itemgetter(2))#According to developers since I want to see easily developers' active years
    for row in toWrite:
        try:
            writer.writerow((row[0], row[1], row[2], row[3]))
        except:
            continue
print('All data is written to the csv file.')
