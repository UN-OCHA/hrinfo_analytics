'''
Prints all organizations (and IDs, if wanted)
'''
import base

def collect_orgs(content, org_info, response):
    if response == 'both':
        for org in content['data']:
            org_info.append((org['id'],org['label']))
    elif response == 'names':
        for org in content['data']:
            org_info.append(org['label'])
    else:
        return "Invalid response"
    return content, org_info, response

def next(content, org_info, response):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        content, org_info, response = collect_orgs(content, org_info, response)
        content, org_info, response = next(content, org_info, response)
    except KeyError:
        pass
    return content, org_info, response

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
    response = input("Do you want organization IDs and names (type 'both') or only organization names (type 'names')? ")
    url = 'https://www.humanitarianresponse.info/en/api/v1.0/organizations?fields=id,label'
    content = base.open_url(url)
    org_info = []
    content, org_info, response = collect_orgs(content, org_info, response)
    content, org_info, response = next(content, org_info, response)
    print(org_info)

if __name__ == '__main__':
   main()
