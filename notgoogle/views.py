from django.http import HttpResponse
from django.shortcuts import render
from django.http import request
import requests
import time

def search_in_other(search):
    pass

def search_in_index(search):
    try: 
        headers = {'Content-Type': 'application/json',}
        data = '{"query":{"match":{"description": "%s"}}}' % (search)
        response = requests.get('http://10.10.100.128:9200/sites/_search'.format(search), headers=headers, data=data)
        json_result = response.json()

        if 'hits' in json_result['hits']:
            hits = []
            for i in json_result['hits']['hits']:
                title = i['_source']['title']
                description = i['_source']['description']
                url = i['_source']['url']
                hit = {"title": title, "description": description, "url": url}
                hits.append(hit)

            if len(hits) > 0:
                return hits
            else:
                return False

    except:
        pass

def index(request):
    try:
        search = request.GET['search']
        if search!="":
            search_start = time.time()
            results = search_in_index(search)
            search_time = "(%s seconds)" % round(time.time()-search_start, 3)

            if results != False:
                return render(request, 'index.html', {"hits":results, "search_time":search_time})
            else:
                return render(request, 'index.html', {"message":"We have not results for your search.", "search_time":search_time})

    except:
        return render(request, 'index.html')
