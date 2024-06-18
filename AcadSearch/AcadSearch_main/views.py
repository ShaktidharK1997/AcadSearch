from django.shortcuts import render
import requests
from requests.exceptions import RequestException
from django.http import JsonResponse
import time
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from AcadSearch_main.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from AcadSearch_main.models import UserSession
from django_redis import get_redis_connection
# Create your views here.

#Remove Hardcoded values later
SEMANTIC_SCHOLAR_API_KEY = '8kxH5DVIYTaE4X2naV3l83RYdf0bYxg7DSFdd7U3'

CORE_API_KEY = '4yDRVsbu3MaJxAfQnWUjXtkHT2NehlKE'

#Search in CORE API
def make_CORE_request(endpoint, query_params = {}):
    url = f'https://api.core.ac.uk/v3/{endpoint}'

    query_params['api-key'] = CORE_API_KEY

    try:
        response = rate_limiting_with_exponential_backoff(url,params = query_params)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(e)
        return None

    
#Search in Semantic Scholar API 
def make_semantic_scholar_request(endpoint, query_params= None):
    url = f'https://api.semanticscholar.org/graph/v1/{endpoint}'
    headers = {'x-api-key': SEMANTIC_SCHOLAR_API_KEY}
    try:
        #response = requests.get(url, params=query_params, headers=headers, timeout=2)
        response = rate_limiting_with_exponential_backoff(url, params=query_params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as e:
        print("The request timed out:", e)
        return None
    except RequestException as e:
        print(e)
        return None

def get_paper_info(request):
    
    query = request.GET.get('paperid')
    source = request.GET.get('source')
    results =  get_paper_details(query, source)

    return JsonResponse(results, safe=False)
    
def get_paper_details(paper_id, source):
    paper_details = {}

    if source == '1':  # Semantic Scholar
        query_params = {
            'fields': 'paperId,title,publicationVenue,year,authors,abstract,citationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,journal,publicationDate'
        }
        result = make_semantic_scholar_request(f'paper/{paper_id}', query_params=query_params)
        print(result)
        if result:
            publication_venue = ""
            download_link = ""
            journal_name = ""
            pub_venue = result.get('publicationVenue', {})
            if pub_venue:
                publication_venue = pub_venue.get('name')

            oap = result.get('openAccessPdf', {})

            if oap:
                download_link = oap.get('url')

            ijournal = result.get('journal', {})
            if ijournal:
                journal_name = ijournal.get('name')



            paper_details = {
                'title': result.get('title', 'No title available'),
                'paperID': result.get('paperId'),
                'year': result.get('year', 'Year not available'),
                'abstract': result.get('abstract', 'Abstract not available'),
                'citationCount': result.get('citationCount', 0),
                'isOpenAccess': result.get('isOpenAccess', False),
                'downloadLink': download_link,
                'authors': result.get('authors', []),
                'publicationVenue': publication_venue,
                'fieldsOfStudy': result.get('fieldsOfStudy', []),
                'journalName': journal_name,
                'publicationDate': result.get('publicationDate', 'No publication date available')
            }
    elif source == '2':  # CORE
        result = make_CORE_request(f'outputs/{paper_id}')
        if result:
            paper_details = {
                'title': result.get('title', 'No title available'),
                'paperID': result.get('id'),
                'year': result.get('yearPublished', 'Year not available'),
                'abstract': result.get('abstract', 'Abstract not available'),
                'citationCount': result.get('citationCount', 0),
                'downloadLink': result.get('downloadUrl', ''),
                'authors': result.get('authors', []),
                'dataProvider': result.get('dataProvider', {}).get('name', 'No data provider available'),
                'publicationDate': result.get('publishedDate', 'No publication date available')
            }

    return paper_details



def get_bulk_paper_details(paper_ids):
    endpoint = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    headers = {'x-api-key': SEMANTIC_SCHOLAR_API_KEY}
    params = {'fields': 'paperId,title,publicationVenue,year,authors,abstract,citationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,journal,publicationDate'}
    data = {"ids": paper_ids}

    try:
        response = requests.post(endpoint, params=params, json=data, headers=headers, timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as e:
        print("The request timed out:", e)
        return None
    except RequestException as e:
        print(e)
        return None
    

def search_articles(request):
    query = request.GET.get('query', '')

    # Prepare to fetch results from Semantic Scholar
    query_params = {'query': query, 'limit': 20}
    api_results_semanticsearch = make_semantic_scholar_request('paper/search', query_params=query_params)

    results = []

    if api_results_semanticsearch and 'data' in api_results_semanticsearch:
        paper_ids_for_batch = [paper['paperId'] for paper in api_results_semanticsearch['data']]
        batch_paper_details = get_bulk_paper_details(paper_ids_for_batch)
        if batch_paper_details:
            for paper_details in batch_paper_details:
                link = ""
                publication_venue_name = ""

                # Check if paper_details is not None
                # Now it's safe to use .get() since paper_details is confirmed to be a dictionary
                if paper_details.get('isOpenAccess'):

                    oapdf = paper_details['openAccessPdf']
                    if oapdf is not None:
                        link=oapdf['url']
                
                pub_venue = paper_details.get('publicationVenue')
                if pub_venue is not None:
                    publication_venue_name = pub_venue.get('name',"")

                paper_info = {
                    'title': paper_details.get('title', 'No title available'),
                    'paperID': paper_details.get('paperId', 'No ID available'),
                    'year': paper_details.get('year', 'Year not available'),
                    'abstract': paper_details.get('abstract', 'Abstract not available'),
                    'authors': paper_details.get('authors', []),
                    'downloadlink': link,
                    'venue' : publication_venue_name,
                    'source' : 1,
                    'citationCount': paper_details.get('citationCount', 0)
                }
                results.append(paper_info)

    # Prepare to fetch results from CORE API
    query_params = {'page': 1, 'pageSize': 4, 'q': query}
    api_results_coresearch = make_CORE_request('search/works', query_params=query_params)

    if api_results_coresearch and 'results' in api_results_coresearch:
        for paper in api_results_coresearch['results']:
            paper_info = {
                'title': paper.get('title', 'No title available'),
                'paperID': paper.get('id', 'No ID available'),
                'year': paper.get('yearPublished', 'Year not available'),
                'abstract': paper.get('abstract', 'Abstract not available'),
                'authors': paper.get('authors', []),
                'downloadlink': paper.get('downloadUrl', ''),
                'source' : 2,
                'citationCount': paper.get('citationCount', 0)
            }
            results.append(paper_info)

    return JsonResponse({'results': results})

#Exponential backoff ratelimiting 

def rate_limiting_with_exponential_backoff(url, params, headers = None,max_retries = 5, initial_wait = 1, backoff_factor = 2):
    retries = 0
    wait_time = initial_wait

    while retries < max_retries:
        try:
            response = requests.get(url, params=params, headers= headers)
            if response.status_code == 200:
                return response  # Return the response if successful
            elif response.status_code == 429 or 500 <= response.status_code < 600:
                # Check if the retry limit has been exceeded
                if retries == max_retries - 1:
                    raise Exception("Maximum retries reached, giving up.")
                # Wait before retrying
                time.sleep(wait_time)
                # Increase the wait time for the next retry
                wait_time *= backoff_factor
                retries += 1
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if retries == max_retries - 1:
                raise Exception(f"API request failed after {max_retries} retries.") from e
            # Wait and retry for other exceptions like timeouts or connection errors
            time.sleep(wait_time)
            wait_time *= backoff_factor
            retries += 1

# Utility function to get tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('email')
            password = data.get('password')
            name = data.get('name')
            institution = data.get('institution')
            dob = data.get('dob')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        user = User.objects.create_user(username=username, email=username, password=password)
        Profile.objects.create(user=user, institution=institution, dob=dob)
        
        return JsonResponse({'message': 'User created successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('email')
            password = data.get('password')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            tokens = get_tokens_for_user(user)
            return JsonResponse({'message': 'Login successful', 'token': tokens['access']}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt

def profile(request):
    if request.method == 'GET':
        username = request.GET.get('user')
        if not username:
            return JsonResponse({'error': 'Username parameter is missing'}, status=400)

        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            return JsonResponse({
                'name': user.username,
                'email': user.email,
                'institution': profile.institution,
                'dob': profile.dob
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Profile does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
#@login_required

def get_online_users(request):
    redis_conn = get_redis_connection("default")
    keys = redis_conn.keys("user:*:online")
    online_user_ids = [int(key.decode().split(':')[1]) for key in keys]
    online_users = User.objects.filter(id__in=online_user_ids).values('username')
    return JsonResponse({'online_users': list(online_users)})

    