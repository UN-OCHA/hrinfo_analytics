'''
Pulls active operations and IDs, used by num_contribs_by_op.py

No-code shortcut for number of active operations on a page:
1) https://www.humanitarianresponse.info/api/v1.0/operations?fields=id,label,status
2) Search "active" (Command+F on Mac)
'''
import urllib.request
import json

def open_url(url):
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    content = json.loads(r.decode('utf-8'))
    return content

def active_ops(content, count_active, active_op_names, active_op_ids):
    for operation in content['data']:
        if operation['status'] == 'active':
            active_op_names.append(operation['label'])
            active_op_ids.append(operation['id'])
            count_active+=1
    return count_active, active_op_names, active_op_ids

def check_next_page(content, count_active, active_op_names, active_op_ids):
    try:
        url = content['next']['href']
        content = open_url(url)
        count_active, active_op_names, active_op_ids = active_ops(content, count_active, active_op_names, active_op_ids)
        count_active, active_op_names, active_op_ids = check_next_page(content, count_active, active_op_names, active_op_ids)
    except KeyError:
        pass
    return count_active, active_op_names, active_op_ids

def main():
    url = 'https://www.humanitarianresponse.info/api/v1.0/operations?fields=id,label,status'
    content = open_url(url)
    count_active = 0
    active_op_names = []
    active_op_ids = []

    count_active, active_op_names, active_op_ids = active_ops(content, count_active, active_op_names, active_op_ids)
    count_active, active_op_names, active_op_ids = check_next_page(content, count_active, active_op_names, active_op_ids)

    # print("Active operations count: ", count_active)
    # print("Names of active ops: ", active_op_names)
    # print("IDs of active ops: ", active_op_ids)
    return active_op_ids, active_op_names

if __name__ == '__main__':
    main()