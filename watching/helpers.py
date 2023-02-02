from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from functools import wraps

from .models import List, Media, Rating, ListItem

# Save base request URL for reuse
baseURL = 'https://api.themoviedb.org/3/'
imageURL = 'https://image.tmdb.org/t/p/'
# Save API key for use in requests
apiKey = '5101df70114a3ec8bc95967d080b3352'
# Image size options
poster_sizes = ["w92", "w154", "w185", "w342", "w500", "w780", "original"]

def listCheck(owner, list):
    # Checks that list exists for given user
    check = List.objects.filter(owner=owner).filter(name=list).count()
    if check > 0:
        return True
    else:
        return False

def listItemCheck(list, itemID):
    # Checks if item is already on list
    check = ListItem.objects.filter(list=list).filter(itemID=itemID).count()
    if check > 0:
        return True
    else:
        return False
    
def ratingCheck(user, subject):
    check = Rating.objects.filter(user=user).filter(subject=subject).count()
    if check > 0:
        return True
    else:
        return False

def getGenre(id, count, type):
    # ID is the genre ID queried for, count is how many genres to return, type is the media type
    # From The Movie Database
    genres = {
        'movie': {
            28: 'Action',
            12: 'Adventure',
            16: 'Animation',
            35: 'Comedy',
            80: 'Crime',
            99: 'Documentary',
            18: 'Drama',
            10751: 'Family',
            14: 'Fantasy',
            36: 'History',
            27: 'Horror',
            10402: 'Music',
            9648: 'Mystery',
            10749: 'Romance',
            878: 'Science Fiction',
            10770: 'TV Movie',
            53: 'Thriller',
            10752: 'War',
            37: 'Western'
        },
        'tv': {
            10759:'Action & Adventure',
            16:'Animation',
            35:'Comedy',
            80:'Crime',
            99:'Documentary',
            18:'Drama',
            10751:'Family',
            10762:'Kids',
            9648:'Mystery',
            10763:'News',
            10764:'Reality',
            10765:'Sci-Fi & Fantasy',
            10766:'Soap',
            10767:'Talk',
            10768:'War & Politics',
            37:'Western'
        }
    }
    if count == 1:
        genre = genres[type][id[0]]
    else:
        genre = []
        for i in range(count):
            genre.append(genres[type][id[i]])

    return genre

def getShow(id):
    url = baseURL + 'tv/' + id
    params = {'api_key': apiKey, 'language': 'en-US'}
    r = requests.get(url = url, params = params)
    r2 = requests.get(url = url + '/watch/providers', params = {'api_key': apiKey})
    show = r.json()
    watch_providers = r2.json()['results']['US']
    show['watch_providers'] = watch_providers
    return show

def getMovie(id):
    url = baseURL + 'movie/' + id
    params = {'api_key': apiKey, 'language': 'en-US'}
    r = requests.get(url = url, params = params)
    movie = r.json()
    return movie

def getProviders(id, type):
    url = baseURL + type + '/' + str(id) + '/watch/providers'
    params = {'api_key': apiKey}
    r = requests.get(url = url, params = params)
    if 'results' in r.json():
        r2 = r.json()['results']
        if 'US' in r2:
            providers = r.json()['results']['US']
        else:
            return False
    else:
        return False
    if 'flatrate' in providers:
        for item in providers['flatrate']:
            item['logo'] = getImage(item['logo_path'], 'original')
    if 'rent' in providers:
        for item in providers['rent']:
            item['logo'] = getImage(item['logo_path'], 'original')
    if 'buy' in providers:
        for item in providers['buy']:
            item['logo'] = getImage(item['logo_path'], 'original')
    return providers

def getImage(APIpath, size = poster_sizes[3]):
    # Check if image already stored in static files

    # If not stored, fetch from TMDB
    url = imageURL + size + APIpath
    r = requests.get(url, stream=True)
    # fs = FileSystemStorage(location=settings.STATIC_ROOT)
    # file = ImageFile()
    # filename = os.path.join(settings.STATIC_URL, 'watching/posters', APIpath[1:])
    # with open(url, 'r') as f:
    #     myfile = ImageFile(f)
    #     for chunk in r.iter_content(chunk_size=128):
    #         myfile.write(chunk)
    return url

def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('browse'))
        return f(request, *args, **kwargs)
    return decorated_function

def constructInfo(data):
    results = {}
    for result in data:
        # Skip person results
        if result['media_type'] == 'person':
            continue

        # Get ID for creating dictionary in results
        id = result['id']
        results[id] = {}
        # Store ID within results for reference and in case of only one object, where outer dictionary will be removed below
        results[id]['id'] = id

        # Get titles
        if result['media_type'] == 'tv':
            results[id]['title'] = result['original_name']
            type = 'tv'
        elif result['media_type'] == 'movie':
            results[id]['title'] = result['title']
            type = 'movie'
        # Save type of media
        results[id]['type'] = type
        # Get Overview
        results[id]['overview'] = result['overview']
        # Get Genre if exists
        if result['genre_ids']:
            results[id]['genre'] = getGenre(result['genre_ids'], 1, type)
        else:
            results[id]['genre'] = None

    # If data is only one result, remove top level of dictionary
    if len(data) == 1:
        keys = results.keys()
        results = results[keys[0]]
    return results

def saveMedia(id, type, poster):
    newMedia = Media(id=id, type=type, poster=poster)
    newMedia.save()

    return True