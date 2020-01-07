import json


name_length = 20
save = json.load(open('test_save.json', 'r+'))

nprs = []
for npr in save['nprs']:
    nprs.append(npr["prefix"])
