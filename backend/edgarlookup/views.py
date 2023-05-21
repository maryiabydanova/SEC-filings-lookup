from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from secedgar.cik_lookup import CIKLookup
from secedgar.utils import make_path
from secedgar.client import NetworkClient
from secedgar.parser import MetaParser
from secedgar import filings, FilingType
from secedgar.exceptions import NoFilingsError
import aiohttp,asyncio,requests,re,json,ssl,os

#don't do this in prod :(
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

user_agent = 'MB (mariabydanova@gmail.com)'
headers = {
    "User-Agent": user_agent
}

def get_companies(request, search_string):
    company_list = _get_companies_list()
    line_pattern = r'^(.*?):(\d+):'
    parsed_company_list=[]
    for company in company_list:
        match = re.match(line_pattern, company)
        if match:
            name = match.group(1)
            cik = match.group(2)
            obj = {'org_name': name, 'org_cik': cik}
            if search_string.lower() in name.lower():
                parsed_company_list.append(obj)
    return JsonResponse({'data': parsed_company_list})

def _get_companies_list():
    data = cache.get('companies_map')
    if data is not None: #check if redis has the data cached
        return data
    else:
        cik_source_data = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt", headers=headers)
        cik_decoded_file_data = cik_source_data.content.decode('iso-8859-1')
        file_lines = cik_decoded_file_data.splitlines() #each line represents a company
        cache.set('companies_map', file_lines, timeout=3600)  # add data to cache with expiration time of 1 hour
        return file_lines

@csrf_exempt
def get_company_filings(request):
    urls = []
    try:
        cik = json.loads(request.body)['cik']
        cik_filings = filings(
            cik_lookup=cik,
            filing_type=FilingType.FILING_10K,
            user_agent=user_agent
        )
        urls = cik_filings.get_urls_safely()[cik]
        urls = list(set(urls))
    except NoFilingsError as e:
        return JsonResponse({'message': 'No Filings found for this organization'})
    return JsonResponse({'data': urls})

@csrf_exempt
def get_filing_data(request):
    body = json.loads(request.body)
    file_url = body['url']
    file_key = body['keyVal']
    download_file(file_url, file_key)
    targetLocation = './parsedFiles/'
    MetaParser().process(os.path.join('./files/', file_key +'.txt'), targetLocation)

    with open(targetLocation + '/' + file_key + '/0.metadata.json') as json_file:
        json_data = json.load(json_file)
        return JsonResponse({'data': json_data})
    

def download_file(url, key):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_download_file(url, key))

async def _download_file(url, key):
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    clien_session = aiohttp.ClientSession(connector=conn, headers=headers,raise_for_status=True)
    client = NetworkClient(user_agent=user_agent)
    response = await client.fetch(url, clien_session)
    with open('./files/' + key + '.txt', "wb") as f:
        f.write(response)

    await clien_session.close()
    await conn.close()
