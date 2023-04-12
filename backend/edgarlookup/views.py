from django.http import HttpResponse
from django.core.cache import cache
from secedgar.cik_lookup import CIKLookup
import requests
import re
import json

def _get_companies_map():
    data = cache.get('companies_map')
    if data is not None:
        print('got cache')
        return data
    else:
        headers = {'User-Agent': 'MB (mariabydanova@gmail.com)'}
        cikSourceData = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt", headers=headers)
        fileData = cikSourceData.content.decode('iso-8859-1')
        lines = fileData.splitlines()
        cache.set('companies_map', lines, timeout=3600)  # add data to cache with expiration time of 1 hour
        return lines

def get_companies(request, search_string):
    lines = _get_companies_map()
    linePattern = r'^(.*?):(\d+):'
    result=[]
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