#@Author: Bilal CAN

from xml.etree import ElementTree as ET
import csv
import os

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
    
all_id = []
all_dev = []
all_desc = []
res_tree = [cdt_res_tree, jdt_res_tree, pde_res_tree, platform_res_tree]
dev_tree = [cdt_dev_tree, jdt_dev_tree, pde_dev_tree, platform_dev_tree]
desc_tree = [cdt_desc_tree, jdt_desc_tree, pde_desc_tree, platform_desc_tree]
all_id01 = []
all_dev01 = []
all_desc01 = []

for traverser in range(4):
    for node in res_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        for child in node.findall('.//update/what'):
            if(child.text == 'FIXED' or child.text == 'WORKSFORME'):
                all_id01.append(report_id)
                break

    for node in dev_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        if report_id in all_id01:
            i = 0;
            for child in node.findall('.//update/what'):
                if i == 1 :
                    all_dev01.append((report_id, child.text))
                i += 1

    for node in desc_tree[traverser].findall('.//report'):
        report_id = node.attrib.get('id')
        for i in range(len(all_dev01)):
            if report_id == all_dev01[i][0]:
                child = node.find('.//update/what')
                all_desc01.append((report_id, child.text))
                break
            
    all_dev.extend(all_dev01)
    all_id.extend(all_id01)
    all_desc.extend(all_desc01)
    all_id01.clear()
    all_dev01.clear()
    all_desc01.clear()
    
print('Developers:', len(all_dev))
print('All reports valid:', len(all_id))
print('Matched reports short desc:', len(all_desc))

if not os.path.exists('Results'):
    os.makedirs('Results')

with open('Results/collected_data.csv', 'w', newline='') as collected_data:
    writer = csv.writer(collected_data, delimiter = '\t')
    writer.writerow(('id', 'developer', 'short_desc'))
    for i in range(len(all_dev)):
        if i % 500 == 0:
            collected_data.flush()
        correct_desc = ""
        for j in range(len(all_desc)):
            if all_dev[i][0] == all_desc[j][0]:
                correct_desc = all_desc[j][1]
                break
        try:
            writer.writerow((all_dev[i][0], all_dev[i][1], correct_desc))
        except:
            continue
print('All data is written to the csv file.')
input()
