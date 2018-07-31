'''
Pulls event counts for all organizations - automated
'''
import content_counts
import base

def counts(num_orgs, org_info, worksheet, rows):

    events_counts = []
    events_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/events?fields=organizations.id&filter[organizations]='

    cell_num = 3
    for index in range(0,num_orgs):
        org_id = org_info[index][0]
        count = 0
        events_full_url = events_base_url + str(org_id)
        content = base.open_url(events_full_url)
        count += len(content['data'])
        content,count = content_counts.next_page(content,count)
        events_counts.append((org_id,count))
        #print(org_id,count)
        cell_num+=1

    events_cells = worksheet.range('D3:D'+rows)
    index = 0
    for cell in events_cells:
        cell.value = events_counts[index][1]
        index+=1
    worksheet.update_cells(events_cells)

    updated = content_counts.update_timestamp(worksheet)
    worksheet.update_acell('D1', updated)

def main():
    num_orgs, org_info, worksheet, rows = content_counts.content()
    counts(num_orgs, org_info, worksheet, rows)

if __name__ == '__main__':
    main()