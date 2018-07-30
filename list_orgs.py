'''
Used for content_counts.py
'''
import base

def collect_orgs(content, org_info):
    for org in content['data']:
        org_info.append((org['id'],org['label']))
    return content, org_info

def next(content, org_info):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        content, org_info = collect_orgs(content, org_info)
        content, org_info = next(content, org_info)
    except KeyError:
        pass
    return content, org_info

def next_page(content, count):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        count += len(content['data'])
        content, count = next_page(content, count)
    except KeyError:
        pass
    return content, count

def main():
    #response = input("Do you want organization IDs and names (type 'both') or only organization names (type 'names')? ")
    url = 'https://www.humanitarianresponse.info/en/api/v1.0/organizations?fields=id,label'
    content = base.open_url(url)
    org_info = []
    content, org_info = collect_orgs(content, org_info)
    content, org_info = next(content, org_info)
    return org_info

if __name__ == '__main__':
   main()
