'''
Pulls assessment counts for all organizations - automated
'''
import content_counts
import base

def counts(num_orgs, org_info, worksheet, rows):

    assess_counts = []
    assess_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/assessments?fields=organizations.id&filter[organizations]='

    cell_num = 3
    for index in range(0,num_orgs):
        org_id = org_info[index][0]
        count = 0
        assess_full_url = assess_base_url + str(org_id)
        content = base.open_url(assess_full_url)
        count += len(content['data'])
        content,count = content_counts.next_page(content,count)
        assess_counts.append((org_id,count))
        #print(org_id,count)
        cell_num+=1

    assess_cells = worksheet.range('E3:E'+rows)
    index = 0
    for cell in assess_cells:
        cell.value = assess_counts[index][1]
        index+=1
    worksheet.update_cells(assess_cells)

    updated = content_counts.update_timestamp(worksheet)
    worksheet.update_acell('E1', updated)

def main():
    num_orgs, org_info, worksheet, rows = content_counts.content()
    counts(num_orgs, org_info, worksheet, rows)

if __name__ == '__main__':
    main()