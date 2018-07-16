'''
Pulls contributing organizations (based on documents, events, maps/infographics) for each year
'''
import base
from gspread.exceptions import APIError
import time
import urllib.request

def next_page(content,years):
    try:
        try:
            url = content['next']['href']
            content = base.open_url(url)
            years = work(content, years)
            years = next_page(content, years)
        except KeyError:
            pass
    except urllib.request.HTTPError:
        try:
            url = content['next']['href']
            print(url)
            content = base.open_url(url)
            years = work(content, years)
            years = next_page(content, years)
        except KeyError:
            pass
    return years

def work(content, years):
    for event in content['data']:
        try:
            # grab the year
            year = int(event['created'])
            year = time.strftime("%Y", time.localtime(year))
            years.setdefault(year, [])

            # grab the organization(s)
            for org in event['organizations']:
                name = org['label']
                if name not in years[year]:
                    years[year].append(name)
                else:
                    continue
        except:
            pass # no year or no org
    return years

def contribs_by_year():

    years = {}

    # events
    events_url = 'https://www.humanitarianresponse.info/en/api/v1.0/events?fields=organizations.label,created'
    content = base.open_url(events_url)
    years = work(content,years)
    years = next_page(content,years)

    # docs
    docs_url = 'https://www.humanitarianresponse.info/api/v1.0/documents?fields=organizations.label,created'
    content = base.open_url(docs_url)
    years = work(content,years)
    years = next_page(content,years)

    # maps/infographics
    maps_url = 'https://www.humanitarianresponse.info/api/v1.0/infographics?fields=organizations.label,created'
    content = base.open_url(maps_url)
    years = work(content,years)
    years = next_page(content,years)

    try:
        worksheet = base.wks.add_worksheet(title="Contribs By Year", rows=100, cols=10)
        # label
        worksheet.update_acell('A1','2012')
        worksheet.update_acell('B1','2013')
        worksheet.update_acell('C1','2014')
        worksheet.update_acell('D1','2015')
        worksheet.update_acell('E1','2016')
        worksheet.update_acell('F1','2017')
        worksheet.update_acell('G1','2018')
    except APIError:
        worksheet = base.wks.worksheet("Contribs By Year")

    # 2012
    orgs = years['2012']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2012'])+1)
    org_cells = worksheet.range('A2:A'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2013
    orgs = years['2013']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2013'])+1)
    org_cells = worksheet.range('B2:B'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2014
    orgs = years['2014']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2014'])+1)
    org_cells = worksheet.range('C2:C'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2015
    orgs = years['2015']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2015'])+1)
    org_cells = worksheet.range('D2:D'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2016
    orgs = years['2016']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2016'])+1)
    org_cells = worksheet.range('E2:E'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2017
    orgs = years['2017']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2017'])+1)
    org_cells = worksheet.range('F2:F'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2018
    orgs = years['2018']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2018'])+1)
    org_cells = worksheet.range('G2:G'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

def main():
    contribs_by_year()

if __name__ == '__main__':
    main()