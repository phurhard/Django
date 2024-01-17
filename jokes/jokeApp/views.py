from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from cachetools import cached, TTLCache

# Create your views here.
url = "https://v2.jokeapi.dev/"

cache = TTLCache(maxsize=2, ttl=3600)
cacheFlag = TTLCache(maxsize=2, ttl=3600)


@cached(cache)
def get_categories():
    res = requests.get(f"{url}categories")
    if res.status_code == 200:
        cacheCategories = res.json()['categories']
        return cacheCategories

    return []


@cached(cacheFlag)
def get_flags():
    res = requests.get(f"{url}flags")
    if res.status_code == 200:
        cacheFlags = res.json()['flags']
        return cacheFlags

    return []


def jokes(request):
    """Render the page"""
    categories = get_categories()
    flags = get_flags()

    if len(categories) or len(flags) != 0:
        pass
    else:
        return JsonResponse({
            'error':  True,
            'message': 'Error fetching details for category'
        }, status=404)

    return render(request, 'home.html', {'categories': categories,
                                         'flags': flags})


def requestJoke(request):
    """Get the required joke"""
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        try:
            data = json.loads(raw_data)
            print(f'Data: {data}')
        except json.JSONDecodeError:
            return JsonResponse({
                'error': True,
                'message': 'Invalid JSON format'
            }, status=400)
        try:
            flags = data.get('flags')
            category = data.get('category')
            print(f'flags: {flags}')
            if len(flags) >= 1:
                flagParams = ','.join(flags)
                params = {'blacklistFlags': flagParams}

                res = requests.get(f'{url}joke/{category}', params=params)
                if res.status_code == 200:
                    response = res.json()

                    return JsonResponse({
                        'error': False,
                        'message': 'Successfully retrieved',
                        'data': response,
                    }, status=200)
                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'Error Handling with flags',
                    }, status=res.status_code)

            else:
                res = requests.get(f'{url}joke/{category}')
                if res.status_code == 200:
                    response = res.json()
                    return JsonResponse({
                        'error': False,
                        'message': 'Successfully retrieved',
                        'data': response,
                    }, status=res.status_code)
                else:
                    print(res.status_code)
                    return JsonResponse({
                        'error': True,
                        'message': 'Error Handling without flags',
                    }, status=res.status_code)
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': str(e),
            }, status=500)
    else:
        return JsonResponse({
            'error': True,
            'message': 'Unsupported request format'
        }, status=405)
