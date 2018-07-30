'''
Pulls the number of contributors per active operation - automated
'''
import base
from gspread.exceptions import APIError
import urllib.request
import active_ops
import time
from datetime import datetime
from pytz import timezone

def pull_contribs(docs_content, contribs):
    for contribution in docs_content['data']:
        # pull organization name if not there already
        try:
            organizations = contribution['organizations']
            for org in organizations:
                org = org['label']
                if org not in contribs:
                    contribs.append(org)
        except TypeError:
            continue
    return contribs

def pull_contribs_next_page(docs_content, contribs):
    try:
        url = docs_content['next']['href']
        content = base.open_url(url)
        contribs = pull_contribs(content, contribs)
        contribs = pull_contribs_next_page(content, contribs)
    except KeyError:
        pass
    return contribs

def num_contribs_by_op(op_ids, op_names):
    try:
        try:
            worksheet = base.wks.add_worksheet(title="Num Contribs By Op", rows=len(op_ids)+1, cols=10)
        except APIError:
            worksheet = base.wks.worksheet("Num Contribs By Op")
        docs_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/documents?filter[operation]='

        # Label
        worksheet.update_acell('A2','Operation')
        worksheet.update_acell('B2','Number of Contributors')

        names_list = worksheet.range('A3:A'+str(len(op_names)+2))
        index = 0
        for cell in names_list:
            cell.value = op_names[index]
            index+=1
        worksheet.update_cells(names_list) # print names

        index = 3
        for op_id in op_ids:
            #print(op_id)
            contribs = [] # list of contributors/organizations
            docs_full_url = docs_base_url + str(op_id)
            docs_content = base.open_url(docs_full_url)
            contribs = pull_contribs(docs_content, contribs)
            contribs = pull_contribs_next_page(docs_content, contribs)
            number = len(contribs)
            #print('index: ', index, ' number: ', number)
            try:
                worksheet.update_cell(index,2,number)
            except APIError:
                time.sleep(10)
                worksheet.update_cell(index,2,number)
            index+=1
    except urllib.request.HTTPError: # if it times out, start over
        return num_contribs_by_op(op_ids, op_names)

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

def main():
    op_ids, op_names = active_ops.main()
    num_contribs_by_op(op_ids, op_names)

if __name__ == '__main__':
    main()