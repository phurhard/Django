from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from typing import List
import logging
from cachetools import cached, TTLCache

# Create your views here.
url = "https://v2.jokeapi.dev/"

cache = TTLCache(maxsize=2, ttl=3600)
cacheFlag = TTLCache(maxsize=2, ttl=3600)


@cached(cache)
def get_categories() -> List[str]:
    '''
    Retrieve categories from the joke API.

    Returns:
        List[str]: A list of categories fetched from the joke API.
    '''
    try:
        res = requests.get(f"{url}categories")
        res.raise_for_status()
        cacheCategories = res.json().get('categories', [])
        return cacheCategories
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching categories: {e}")
    except ValueError as e:
        logging.error(f"Error parsing JSON response: {e}")
    return []


@cached(cacheFlag)
def get_flags() -> List[str]:
    '''
    Retrieve a list of flags from the joke API and
    cache the result using the specified TTL cache.
    Returns the list of flags fetched from the API.
    If an error occurs during the process,
    appropriate error messages are logged, and an empty list is returned.
'''
    try:
        res = requests.get(f"{url}flags")
        res.raise_for_status()
        cacheFlags = res.json().get('flags', [])
        return cacheFlags
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching flags: {e}")
    except ValueError as e:
        logging.error(f"Error parsing JSON response: {e}")
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
            # print(f'Data: {data}')
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON format'
            }, status=400)
        try:
            flags = data.get('flags')
            category = data.get('category')
            # print(f'flags: {flags}')
            if len(flags) >= 1:
                flagParams = ','.join(flags)
                params = {'blacklistFlags': flagParams}

                res = requests.get(f'{url}joke/{category}', params=params)
                if res.status_code == 200:
                    response = res.json()

                    return JsonResponse({
                        'success': True,
                        'message': 'Successfully retrieved',
                        'data': response,
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Error Handling with flags',
                    }, status=res.status_code)

            else:
                res = requests.get(f'{url}joke/{category}')
                if res.status_code == 200:
                    response = res.json()
                    return JsonResponse({
                        'success': True,
                        'message': 'Successfully retrieved',
                        'data': response,
                    }, status=res.status_code)
                else:
                    # print(res.status_code)
                    return JsonResponse({
                        'success': False,
                        'message': 'Error Handling without flags',
                    }, status=res.status_code)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
            }, status=500)
    elif request.method == "GET":
        return jokes(request)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Unsupported request format'
        }, status=415)
