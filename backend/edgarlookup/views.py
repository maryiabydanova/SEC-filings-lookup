from django.http import HttpResponse
from secedgar.cik_lookup import CIKLookup
import requests
import re

import json

def get_companies(request, search_string):
    headers = {'User-Agent': 'MB (mariabydanova@gmail.com)'}
    cikSourceData = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt", headers=headers)
    fileData = cikSourceData.content.decode('iso-8859-1')
    result = []
    linePattern = r'^(.*?):(\d+):'
    lines = fileData.splitlines()
    for line in lines:
        match = re.match(linePattern, line)
        if match:
            name = match.group(1)
            cik = match.group(2)
            obj = {'org_name': name, 'org_cik': cik}
            if search_string.lower() in name.lower():
                result.append(obj)
    json_data = json.dumps(result)
    return HttpResponse(json_data, content_type='application/json')

def get_cik_possibilities(request, my_string):
    initial_cik_lookup = CIKLookup(lookups=[my_string], user_agent="MB (mariabydanova@gmail.com)")
    print('v', initial_cik_lookup.get_cik_map())
    if len(initial_cik_lookup.ciks) > 0 : 
        lookup = initial_cik_lookup.lookups[0]
        soup = initial_cik_lookup._get_lookup_soup(lookup)
        cik_possibilities = initial_cik_lookup._get_cik_possibilities(soup)
        result = ','.join(cik_possibilities)
    else:
        result = cik_lookup.ciks

    return HttpResponse(result)