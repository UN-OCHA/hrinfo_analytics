'''
Pulls the number of contributions per active operation
'''
import base
from gspread.exceptions import APIError
import urllib.request
import active_ops
import time

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
            # label
            worksheet.update_acell('A1','Operation')
            worksheet.update_acell('B1','Number of Contributors')
        except APIError:
            worksheet = base.wks.worksheet("Num Contribs By Op")
        docs_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/documents?filter[operation]='

        names_list = worksheet.range('A1:A'+str(len(op_names)+1))
        index = 0
        for cell in names_list:
            cell.value = op_names[index]
            index+=1
        worksheet.update_cells(names_list) # print names

        index = 0
        for op_id in op_ids:
            print(op_id)
            contribs = [] # list of contributors/organizations
            docs_full_url = docs_base_url + str(op_id)
            docs_content = base.open_url(docs_full_url)
            contribs = pull_contribs(docs_content, contribs)
            contribs = pull_contribs_next_page(docs_content, contribs)
            number = len(contribs)
            try:
                worksheet.update_cell(index,2,number)
            except APIError:
                time.sleep(10)
                worksheet.update_cell(index,2,number)
            index+=1
    except urllib.request.HTTPError: # if it times out, start over
        return num_contribs_by_op(op_ids, op_names)

def main():
    op_ids, op_names = active_ops.main()
    num_contribs_by_op(op_ids, op_names)

if __name__ == '__main__':
    main()