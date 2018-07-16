'''
Pulls all groups (sectors, clusters, sub-clusters) by operation, including date last modified
'''
import base
import time
from gspread.exceptions import APIError

def compiling(dict):

    # Upload to Sheets
    rows = len(dict)+5
    try:
        worksheet = base.wks.add_worksheet(title="Groups By Operation", rows=str(rows), cols="10")
    except APIError:
        worksheet = base.wks.worksheet("Groups By Operation")

    # label
    worksheet.update_acell('A1','Operation')
    worksheet.update_acell('B1','Name')
    worksheet.update_acell('C1','Type')
    worksheet.update_acell('D1','Last Modified')

    # Dict to list
    mylist = []
    for key, value in dict.items():
        temp = [key,value]
        mylist.append(temp)

    # total number of rows depends on total number of groups
    rows = 0
    for operation in mylist:
        rows += len(operation[1])
    rows = str(rows+1)

    op_list = worksheet.range('A2:A'+rows)
    name_list = worksheet.range('B2:B'+rows)
    type_list = worksheet.range('C2:C'+rows)
    time_list = worksheet.range('D2:D'+rows)

    op_list_index = 0
    index = 0
    for operation in mylist:
        within_op_index = 0
        op_name = operation[0]
        num_clusters = len(operation[1])
        same_op = True
        cell = op_list[op_list_index]
        name_cell = name_list[index]
        type_cell = type_list[index]
        time_cell = time_list[index]
        clus_name = operation[1][within_op_index][0]
        type_name = operation[1][within_op_index][1]
        time_name = operation[1][within_op_index][2]
        name_cell.value = clus_name
        type_cell.value = type_name
        time_cell.value = time_name
        cluster_index = 0
        while same_op:
            cell.value = op_name
            op_list_index+=1
            cluster_index+=1
            index+=1
            within_op_index+=1
            if cluster_index == num_clusters:
                same_op = False
                continue
            cell = op_list[op_list_index]
            name_cell = name_list[index]
            type_cell = type_list[index]
            time_cell = time_list[index]
            clus_name = operation[1][within_op_index][0]
            type_name = operation[1][within_op_index][1]
            time_name = operation[1][within_op_index][2]
            name_cell.value = clus_name
            type_cell.value = type_name
            time_cell.value = time_name

    # Update in batch - avoids API timeout problem
    worksheet.update_cells(op_list)
    worksheet.update_cells(name_list)
    worksheet.update_cells(type_list)
    worksheet.update_cells(time_list)
    exit()

def next_page(content, dict, index):
    index+=1
    url = 'https://www.humanitarianresponse.info/en/api/v1.0/bundles?page%5Bnumber%5D=' + str(index)

    try:
        content = base.open_url(url)
        if len(content['data']) == 0:
            compiling(dict)
        dict,index = compile_clusters(content, dict, index)
        dict,index = next_page(content, dict, index)
    except KeyError:
        pass

    return dict,index

def compile_clusters(content, dict, index):
    for group in content['data']:
        try:
            operation = group['operation'][0]['label']
        except TypeError: # operation is null, don't include
            continue # goes to next group

        # pull name of group
        try:
            name = group['global_cluster']['label']
        except KeyError:
            name = group['label']

        type = group['type']

        last_modified = int(group['changed'])
        last_modified = time.strftime("%Y %d %b", time.localtime(last_modified))

        if operation not in dict:  # cluster's operation not in dictionary already
            key = operation
            dict.setdefault(key, [])
            dict[key].append((name,type,last_modified))  # map the cluster to the operation
        else:  # operation is already in there
            dict[operation].append((name,type,last_modified))
    return dict, index

def groups_by_op(base_url):
    index = 1
    content = base.open_url(base_url+str(index))
    dict = {}
    dict,index = compile_clusters(content, dict, index)
    next_page(content, dict,index)

if __name__ == '__main__':
    base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/bundles?page%5Bnumber%5D='
    groups_by_op(base_url)