import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd

usr = 'takaakira.yamauchi'
pw = ''

# {'id': '780062866', 'type': 'page', 'status': 'current', 'title': 'Domo Official Portal', 'extensions': {'position': 3}, '_links': {'webui': '/display/RPM/Domo+Official+Portal', 'edit': '/pages/resumedraft.action?draftId=780062866', 'tinyui': '/x/ktB_Lg', 'self': 'https://confluence.rakuten-it.com/confluence/rest/api/content/780062866'}, '_expandable': {'container': '/rest/api/space/RPM', 'metadata': '', 'operations': '', 'children': '/rest/api/content/780062866/child', 'restrictions': '/rest/api/content/780062866/restriction/byOperation', 'history': '/rest/api/content/780062866/history', 'ancestors': '', 'body': '', 'version': '', 'descendants': '/rest/api/content/780062866/descendant', 'space': '/rest/api/space/RPM'}}


def call_api(url):
    limit = 100
    i = 0
    flag = True
    arr = []
    while flag:
        conflu_url = url + '?limit={0}&start={1}'.format(
            limit, i)
        i = i+limit
        res = requests.get(conflu_url, auth=HTTPBasicAuth(usr, pw))
        if res.status_code != 200:
            return arr
        r = res.text
        j = json.loads(r)
        m = 0
        for x in j['results']:
            d = {}
            m = m+1
            d['title'] = x['title']
            d['child'] = x['_expandable']['children']
            arr.append(d)

        if m < limit:
            flag = False
    return arr


def find_page(page_name):
    limit = 100
    i = 0
    flag = True
    tg = None
    while flag:
        conflu_url = 'https://confluence.rakuten-it.com/confluence/rest/api/space/RPM/content/page?limit={0}&start={1}'.format(
            limit, i)
        i = i+limit
        res = requests.get(conflu_url, auth=HTTPBasicAuth(usr, pw))
        r = res.text
        j = json.loads(r)
        for x in j['results']:
            title = x['title']
            if title == page_name:
                print(x)
                tg = x
                flag = False
    return tg


def page_tree(parent, ptitle):
    d = {'parent': ptitle}
    conflu_url = 'https://confluence.rakuten-it.com/confluence{0}/page'.format(parent)
    r = call_api(conflu_url)
    d['children'] = r
    return d


def listing_all_pages(topID, topTitle, is_deeper):
    def deeper(res, m):
        l = len(res['children'])
        i = 0
        m = m+1
        while i < l:
            p = res['children'][i]['child']
            t = res['children'][i]['title']
            resp = page_tree(p, t)
            resp['depth'] = m
            arr.append(resp)
            deeper(resp, m)
            i = i + 1

    arr = []
    r = page_tree(topID, topTitle)
    r['depth'] = 0
    arr.append(r)
    for row in r['children']:
        m = 1
        parent = row['child']
        res = page_tree(parent, row['title'])
        res['depth'] = m
        arr.append(res)

        if is_deeper:
            deeper(res, m)
    return arr


if __name__ == '__main__':
    pn = 'Domo Official Portal'
    # tg = find_page(pn)

    DOMO_TOP_ID = '/rest/api/content/780062866/child'
    is_deeper = True
    arr = listing_all_pages(DOMO_TOP_ID, pn, is_deeper)
    titles = []
    children = []
    depth = []
    for x in arr:
        titles.append(x['parent'])
        depth.append(x['depth'])
        c = []
        for row in x['children']:
            c.append(row['title'])
        children.append('; '.join(c))
    di = {'Title': titles, 'depth': depth, 'Child_Page': children}
    df = pd.DataFrame(di)
    df.to_excel('DOMO conflu page tree.xlsx')

# {'parent': 'Some Tips for Creating Cards in Domo', 'children': [{'title': '10. If you want to copy card', 'child': '/rest/api/content/776447603/child'}, {'title': '11. If you want to show the sum of category in Stacked Bar Chart Card', 'child': '/rest/api/content/776447821/child'}, {'title': '12. How to connect the teradata.', 'child': '/rest/api/content/1986218593/child'}, {'title': '1. If you want to remove Max, Min, Ave value', 'child': '/rest/api/content/776446420/child'}, {'title': '2. If you want the current value as Summary Number', 'child': '/rest/api/content/776446544/child'}, {'title': '3. If you want to create accumulated GMS card', 'child': '/rest/api/content/776446579/child'}, {'title': '4. If you want to create a world map card', 'child': '/rest/api/content/776446647/child'}, {'title': '5. If you want to create a Barï¼‹Line Chart card', 'child': '/rest/api/content/776446667/child'}, {'title': '6. If you want to set the display unit', 'child': '/rest/api/content/776446694/child'}, {'title': '7. If you want to check what types of dataset can be uploaded to Domo', 'child': '/rest/api/content/776446722/child'}, {'title': '8. If you want to add a new collection', 'child': '/rest/api/content/776446764/child'}, {'title': '9. If you want to change the number of lines in Bar+Line Chart', 'child': '/rest/api/content/776446860/child'}]}
