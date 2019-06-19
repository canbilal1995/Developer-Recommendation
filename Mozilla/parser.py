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
