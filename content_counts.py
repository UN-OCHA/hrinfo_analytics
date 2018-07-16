'''
Pulls counts of different content types for all organizations
'''
import base
from gspread.exceptions import APIError

def collect_orgs(content, org_info):
    for org in content['data']:
        org_info.append((org['id'],org['label']))
    return content, org_info

def list_of_orgs():
    url = 'https://www.humanitarianresponse.info/en/api/v1.0/organizations?fields=id,label'
    content = base.open_url(url)
    org_info = []
    content, org_info = collect_orgs(content, org_info)
    content, org_info = next(content, org_info)
    return org_info

def next_page(content, count):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        count += len(content['data'])
        content, count = next_page(content, count)
    except KeyError:
        pass
    return content, count

def content(org_info):
    rows = str(len(org_info)+1)

    # open sheet
    try:
        worksheet = base.wks.add_worksheet(title="Content By Org", rows=(len(org_info)+1), cols=10)
        # label
        worksheet.update_acell('A1','Organization')
        worksheet.update_acell('B1','Documents')
        worksheet.update_acell('C1','Maps/Infographics')
        worksheet.update_acell('D1','Events')
        worksheet.update_acell('E1','Assessments')
        worksheet.update_acell('F1','Total Content')
    except APIError:
        worksheet = base.wks.worksheet("Content By Org")

    # organizations
    name_cells = worksheet.range('A2:A'+rows)
    index = 0
    for cell in name_cells:
        cell.value = org_info[index][1]
        index+=1
    worksheet.update_cells(name_cells)

    # DOCUMENTS
    doc_counts = []
    docs_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/documents?fields=organizations.id&filter[organizations]='

    # to modify to run from 155, change range to start to 155-2
    cell_num = 2 # exact starting cell
    for index in range(0,4525): #subtract 2 from start, 1 from end
        org_id = org_info[index][0]
        org_name = org_info[index][1]
        print(org_id, org_name)
        count = 0
        docs_full_url = docs_base_url + str(org_id)
        content = base.open_url(docs_full_url)
        count += len(content['data'])
        content,count = next_page(content,count)
        doc_counts.append((org_id,count))
        cell_num+=1

    doc_cells = worksheet.range('B2:B4526') #put exact cells here, inclusive
    index = 0
    for cell in doc_cells:
        cell.value = doc_counts[index][1]
        index+=1
    worksheet.update_cells(doc_cells)

    # MAPS/INFOGRAPHICS
    map_counts = []
    maps_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/infographics?fields=organizations.id&filter[organizations]='

    # to modify to run from 155, change range to start to 155-2
    cell_num = 2 # exact starting cell
    for index in range(0,4525): # subtract 2 from start, 1 from end
        org_id = org_info[index][0]
        org_name = org_info[index][1]
        print(org_id, org_name)
        count = 0
        maps_full_url = maps_base_url + str(org_id)
        content = base.open_url(maps_full_url)
        count += len(content['data'])
        content,count = next_page(content,count)
        map_counts.append((org_id,count))
        cell_num+=1

    map_cells = worksheet.range('C2:C4526') #put exact cells here, inclusive
    index = 0
    for cell in map_cells:
        cell.value = map_counts[index][1]
        index+=1
    worksheet.update_cells(map_cells)

    # EVENTS
    events_counts = []
    events_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/events?fields=organizations.id&filter[organizations]='

    # to modify to run from 155, change range to start to 155-2
    cell_num = 2 # exact starting cell
    for index in range(0,4525): # subtract 2 from start, 1 from end
        org_id = org_info[index][0]
        org_name = org_info[index][1]
        print(org_id, org_name)
        count = 0
        events_full_url = events_base_url + str(org_id)
        content = base.open_url(events_full_url)
        count += len(content['data'])
        content,count = next_page(content,count)
        events_counts.append((org_id,count))
        cell_num+=1

    events_cells = worksheet.range('D2:D4526') #put exact cells here, inclusive
    index = 0
    for cell in events_cells:
        cell.value = events_counts[index][1]
        index+=1
    worksheet.update_cells(events_cells)

    # ASSESSMENTS
    assess_counts = []
    assess_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/assessments?fields=organizations.id&filter[organizations]='

    # to modify to run from 155, change range to start to 155-2
    cell_num = 2 #exact starting cell
    for index in range(0,4525): #subtract 2 from start, 1 from end
        org_id = org_info[index][0]
        org_name = org_info[index][1]
        print(org_id, org_name)
        count = 0
        assess_full_url = assess_base_url + str(org_id)
        content = base.open_url(assess_full_url)
        count += len(content['data'])
        content,count = next_page(content,count)
        assess_counts.append((org_id,count))
        cell_num+=1

    assess_cells = worksheet.range('E2:E4526') #put exact cells here, inclusive
    index = 0
    for cell in assess_cells:
        cell.value = assess_counts[index][1]
        index+=1
    worksheet.update_cells(assess_cells)

def main():
    org_info = list_of_orgs()
    content(org_info)

if __name__ == '__main__':
    main()