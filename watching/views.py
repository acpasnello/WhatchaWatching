from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from sqlite3 import IntegrityError
import requests
import json

from FinalProject.keys import api_key
from .models import User, List, ListItem, Rating
from friends.models import Relationship, Activity
from .forms import ListForm
from .helpers import getGenre, getImage, constructInfo, listCheck, getShow, getMovie, getProviders, ratingCheck

# Save base request URL for reuse
baseURL = "https://api.themoviedb.org/3/"
# Save TMDB API key for use in requests
apiKey = api_key

# Create your views here.
def index(request):
    # Get active user
    user = User.objects.get(pk=request.user.id)
    # Get watchlist
    watchlist = List.objects.filter(owner=user).get(name='Watchlist').listitems.all()
    # Set up request info
    partialURL = baseURL + 'discover/'
    popularityParams = {'api_key': apiKey, 'sort_by': 'popularity.desc', 'include_adult': False, 'page': 1}
    moviesURL = partialURL + 'movie'
    showsURL = partialURL + 'tv'
    # Get currently popular movie list
    popMoviesRequest = requests.get(url = moviesURL, params = popularityParams)
    popMovies = popMoviesRequest.json()
    popMovies = popMovies['results']
    # Get currently popular show list
    popShowsRequest = requests.get(url = showsURL, params = popularityParams)
    popShows = popShowsRequest.json()
    popShows = popShows['results']
    # Get activity
    # Get user's friend relationships
    friendsquery = Relationship.objects.filter(type='F').filter(Q(user_first=user) | Q(user_second=user))
    friendIDS = []
    for ship in friendsquery:
        other = ship.otherUser(user)
        friendIDS.append(other.pk)
    friends = User.objects.filter(pk__in=friendIDS)
    activities = Activity.objects.filter(user__in=friends).order_by('-when')
    serializeddata = [activity.serialize() for activity in activities]
    return render(request, 'watching/index.html', {'watchlist': watchlist, 'movielist': popMovies, 'showlist': popShows, 'activity': serializeddata})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("browse"))
        else:
            return render(request, "watching/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "watching/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "watching/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create Watchlist, Favorites, and Watched Lists for new user
            watchlist = List.objects.create(name='Watchlist', description="To watch soon", owner=user)
            watchlist.save()
            favorites = List.objects.create(name='Favorites', description='My all-time favorites', owner=user)
            favorites.save()
            watched = List.objects.create(name='Watched', description='Already seen', owner=user)
            watched.save()
        except IntegrityError:
            return render(request, "watching/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "watching/register.html")

def browse(request):
    # Get top rated movies
    partialURL = baseURL + 'discover/'
    popularityParams = {'api_key': apiKey, 'sort_by': 'popularity.desc', 'include_adult': False, 'page': 1}
    topRatedParams = {'api_key': apiKey, 'sort_by': 'vote_average.desc', 'include_adult': False, 'page': 1, 'watch_region': 'US', 'vote_count.gte': 300}
    moviesURL = partialURL + 'movie'
    showsURL = partialURL + 'tv'
    popMoviesRequest = requests.get(url = moviesURL, params = popularityParams)
    topRatedMoviesRequest = requests.get(url= moviesURL, params = topRatedParams)
    popShowsRequest = requests.get(url = showsURL, params = popularityParams)
    topRatedShowsRequest = requests.get(url = showsURL, params = topRatedParams)
    # Get Popular Movies
    popMovies = popMoviesRequest.json()
    popMovies = popMovies['results']
    # Get Top Rated Movies
    topMovies = topRatedMoviesRequest.json()
    topMovies = topMovies['results']
    # Get Popular Shows
    popShows = popShowsRequest.json()
    popShows = popShows['results']
    # Get Top Rated Shows
    topShows = topRatedShowsRequest.json()
    topShows = topShows['results']

    return render(request, 'watching/browse.html', {'topMovies': topMovies, 'topShows': topShows, 'popMovies': popMovies, 'popShows': popShows})

def createlist(request):
    if request.method == "POST":
        # Get submitted criteria
        name = request.POST['name']
        description = request.POST['description']
        # Check list with this name doesn't already exist
        listcheck = List.objects.filter(name=name).filter(owner=request.user).count()
        if listcheck > 0:
            return render(request, 'watching/viewlist.html', {'message': 'A list with this name already exisits!'})
        else:
            # Create new list
            list = List.objects.create(name=name, description=description, owner=request.user)
            list.save()
        # Render display of newly-created list
        return HttpResponseRedirect(reverse('viewlist', args=[list.owner.pk, name]))
    else:
        form = ListForm()
        return render(request, 'watching/createlist.html', {'form': form})

def editlist(request, name):
    if request.method == 'POST':
        id = request.POST['id']
        listname = request.POST['name']
        user = request.user
        description = request.POST['description']
        list = List.objects.get(pk=id)
        list.name = listname
        list.description = description
        list.save()
        return HttpResponseRedirect(reverse('viewlist', args=[list.owner.pk, list.name]))
    else:
        check = listCheck(request.user, name)
        if check:
            list = List.objects.filter(owner=request.user).get(name=name)
            form = ListForm(instance=list)
            return render(request, 'watching/editlist.html', {'form': form, 'id': list.pk, 'name': list.name})
        else:
            return render(request, 'watching/viewlist.html', {'message': 'This list does not exist'})
    pass

def viewlist(request, userid, name):
    owner = User.objects.get(pk=userid)
    # Check list exists
    listcheck = listCheck(owner, name)
    # Is viewer owner?
    requester = request.user
    if requester == owner:
        ownerviewing = True
    else:
        ownerviewing = False
    if listcheck:
        list = List.objects.filter(owner=owner).get(name=name)
        # if ListItem.objects.filter(list=list.pk).count() > 0:
        items = ListItem.objects.filter(list=list.pk)
        return render(request, 'watching/viewlist.html', {'list': list, 'items': items, 'ownerviewing': ownerviewing, 'owner': owner})
        # else:
            # return render(request, 'watching/viewlist.html', {'list': list})

    else:
        return render(request, 'watching/viewlist.html', {'message': 'This list does not exist', 'owner': owner})

def mylists(request):
    # Get user's lists
    user = User.objects.get(pk=request.user.id)
    lists = user.mylists.all()

    return render(request, 'watching/mylists.html', {'lists': lists})

def search(request):
    url = baseURL + 'search/multi'
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('query') is not None:
            query = data['query']
            print(query)
            headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
            params = {'api_key': apiKey, 'language': 'en-US', 'query': query, 'page': 1, 'include_adult': 'false'}
            searchRequest = requests.get(url = url, params = params, headers=headers)
            print("API responded")
            results = searchRequest.json()['results']
            response = JsonResponse(results, safe=False)
            return response
        else:
            return HttpResponseRedirect(reverse('browse'))
    else:
        query = request.GET['query']
        headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
        params = {'api_key': apiKey, 'language': 'en-US', 'query': query, 'page': 1, 'include_adult': 'false'}
        searchRequest = requests.get(url = url, params = params, headers=headers)
        data = searchRequest.json()['results']
        results = {}
        for result in data:
            # Skip person results
            if result['media_type'] == 'person':
                continue

            id = result['id']
            results[id] = {}

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
            # Get Poster if exists
            if result['poster_path']:
                results[id]['poster_path'] = result['poster_path']
        return render(request, "watching/searchresults.html", {'results': results, 'query': query})

def details(request, type, id):
    if type == 'M':
        type = 'movie'
    elif type == 'S':
        type = 'tv'
    url = baseURL + type + '/' + str(id)
    params = {'api_key': apiKey}
    r = requests.get(url = url, params = params)
    # if r.status_code == requests.codes.ok:
    data = r.json()
    # Get poster if available
    if data['poster_path']:
        url = getImage(data['poster_path'], 'w185')
    else:
        url = None
    # Get watch providers
    providers = getProviders(id, type)
    # Check for rating
    rating = None
    if ratingCheck(request.user.id, id):
       rating = Rating.objects.filter(user=request.user.id).get(subject=id)

    # Render correct details page
    if type == 'movie':
        return render(request, "watching/moviedetails.html", {'data': data, 'poster': url, 'providers': providers, 'rating': rating})
    elif type == 'tv':
        return render(request, "watching/tvdetails.html", {'data': data, 'poster': url, 'providers': providers, 'rating': rating})

def addtolist(request):
    # Requires listname, id, type submitted through a Form
    if request.method == 'POST':
        listname = request.POST['list']
        id = request.POST['id']
        type = request.POST['type']
        poster = request.POST['poster']
        # Check list exists
        listcheck = listCheck(request.user, listname)
        if listcheck:
            list = List.objects.filter(owner=request.user).get(name=listname)
            typechoice = None
            name = None
            if type.lower() == 'movie':
                r = getMovie(id)
                name = r['title']
                typechoice = 'M'
            elif type.lower() == 'tv':
                r = getShow(id)
                name = r['original_name']
                typechoice = 'S'
            newitem = ListItem(list = list, itemID = id, name = name, type = typechoice, poster = poster)
            newitem.save()
        else:
            return render(request, 'watching/viewlist.html', {'message': 'The list you are trying to add to does not exist!'})

        return HttpResponseRedirect(reverse('viewlist', args=[list.owner.pk, list.name]))
    
    else:
        return HttpResponseRedirect(reverse('index'))

def removefromlist(request):
    if request.method == 'POST':
        # Get submitted info
        listname = request.POST['list']
        id = request.POST['id']
        # Get list instance
        list = List.objects.filter(name=listname).get(owner=request.user)
        # Confirm list owner is requesting user
        user = request.user
        if user == list.owner:
            item = ListItem.objects.filter(list=list).filter(itemID=id)
            item.delete()
            return HttpResponseRedirect(reverse('viewlist', args=[list.owner.pk, listname]))
        else:
            return render(request, 'watching/viewlist.html', {'message': 'You do not own this list!'})
        
    else:
        return render(request, 'watching/viewlist.html', {'message': 'No, no, no, not today.'})

def getposterpath(request):
    jsondata = json.loads(request.body)
    activityID = jsondata.get('id')
    print(activityID)
    activity = Activity.objects.get(pk=activityID)
    if activity.subjecttype == 'M':
        data = getMovie(activity.subject)
    elif activity.subjecttype == 'S':
        data = getMovie(activity.subject)
    if data['poster_path']:
        poster = {'url': getImage(data['poster_path'], 'w185')}
    else:
        poster = {'url': None}
    response = JsonResponse(poster, safe=False)
    return response