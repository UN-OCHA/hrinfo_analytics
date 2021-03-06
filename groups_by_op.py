'''
Pulls all groups (sectors, clusters, sub-clusters) by operation, including date last modified - automated
'''
import base
import time
from gspread.exceptions import APIError
from datetime import datetime
from pytz import timezone

def compiling(dict):

    spreadsheet = base.get_spreadsheet()
    # Upload to Sheets
    try:
        worksheet = spreadsheet.add_worksheet(title="Groups By Active Operation", rows=500, cols=10)
    except APIError:
        worksheet = spreadsheet.worksheet("Groups By Active Operation")

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # label
    worksheet.update_acell('A2','Operation')
    worksheet.update_acell('B2','Name')
    worksheet.update_acell('C2','Type')
    worksheet.update_acell('D2','Last Modified')
    worksheet.update_acell('E2','Created')
    worksheet.update_acell('F2','Published?')

    # Dict to list
    mylist = []
    for key, value in dict.items():
        temp = [key,value]
        mylist.append(temp)

    # total number of rows depends on total number of groups
    rows = 0
    for operation in mylist:
        rows += len(operation[1])
    rows = str(rows+2)

    op_list = worksheet.range('A3:A'+rows)
    name_list = worksheet.range('B3:B'+rows)
    type_list = worksheet.range('C3:C'+rows)
    time_list = worksheet.range('D3:D'+rows)
    create_list = worksheet.range('E3:E'+rows)
    pub_list = worksheet.range('F3:F'+rows)

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
        create_cell = create_list[index]
        pub_cell = pub_list[index]
        clus_name = operation[1][within_op_index][0]
        type_name = operation[1][within_op_index][1]
        time_name = operation[1][within_op_index][2]
        create_name = operation[1][within_op_index][3]
        pub_name = operation[1][within_op_index][4]
        name_cell.value = clus_name
        type_cell.value = type_name
        time_cell.value = time_name
        create_cell.value = create_name
        pub_cell.value = pub_name
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
            create_cell = create_list[index]
            pub_cell = pub_list[index]
            clus_name = operation[1][within_op_index][0]
            type_name = operation[1][within_op_index][1]
            time_name = operation[1][within_op_index][2]
            create_name = operation[1][within_op_index][3]
            pub_name = operation[1][within_op_index][4]
            name_cell.value = clus_name
            type_cell.value = type_name
            time_cell.value = time_name
            create_cell.value = create_name
            pub_cell.value = pub_name

    # Update in batch - avoids API timeout problem
    worksheet.update_cells(op_list)
    worksheet.update_cells(name_list)
    worksheet.update_cells(type_list)
    worksheet.update_cells(time_list)
    worksheet.update_cells(create_list)
    worksheet.update_cells(pub_list)
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
        last_modified = time.strftime("%d-%b-%Y", time.localtime(last_modified))

        created = int(group['created'])
        created = time.strftime("%d-%b-%Y", time.localtime(created))

        published = int(group['published'])
        if published == 1:
            pub_stat = "Yes"
        elif published == 0:
            pub_stat = "No"
        else:
            pub_stat = ""

        if operation not in dict:  # cluster's operation not in dictionary already
            key = operation
            dict.setdefault(key, [])
            dict[key].append((name,type,last_modified,created,pub_stat))  # map the cluster to the operation
        else:  # operation is already in there
            dict[operation].append((name,type,last_modified,created,pub_stat))
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
