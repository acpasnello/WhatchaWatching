from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json


from .helpers import logActivity, orderUsers, checkShip, buttonFiller
from watching.helpers import ratingCheck
from watching.models import User, Rating
from .models import Relationship, Activity

# Create your views here.

# Relationship Types
PENDING_FIRST_SECOND = 'PFS'
PENDING_SECOND_FIRST = 'PSF'
FRIENDS = 'F'
BLOCK_FIRST_SECOND = 'BFS'
BLOCK_SECOND_FIRST = 'BSF'
BLOCK_BOTH = 'BB'

def index(request):
    # Get active user
    user = User.objects.get(pk=request.user.id)
    friends = []
    actions = {}
    formactions = {}
    labels = {}
    values = {}
    receivers = {}
    # Search relationships for their friends, need to search with user in both possible user slots
    friendsquery = Relationship.objects.filter(type=FRIENDS).filter(Q(user_first=user) | Q(user_second=user))
    for item in friendsquery:
        # User info
        userid = item.otherUser(user).id
        username = item.otherUser(user).username
        since = item.lastupdated
        friends.append({'username': username, 'userid': userid, 'since': since})
        # Construct form info
        action = item.actions(user)
        actions[username] = action
        if item.position(user) == 1:
            subjectUser = item.user_second
        elif item.position(user) == 2:
            subjectUser = item.user_first
        button = buttonFiller(user, subjectUser, item)
        formactions[username] = button['formaction']
        if button['label']:
            labels[username] = button['label']
        values[username] = button['value']
        receivers[username] = button['receiver']
    # Get sent requests
    sentRequests = Relationship.objects.filter((Q(user_first=user) & Q(type=PENDING_FIRST_SECOND)) | (Q(user_second=user) & Q(type=PENDING_SECOND_FIRST)))
    # Get incoming requests
    incRequests = Relationship.objects.filter((Q(user_first=user) & Q(type=PENDING_SECOND_FIRST)) | (Q(user_second=user) & Q(type=PENDING_FIRST_SECOND)))
    for req in sentRequests:
        action = req.actions(user)
        actions[req.pk] = action
        if req.position(user) == 1:
            subjectUser = req.user_second
        elif req.position(user) == 2:
            subjectUser = req.user_first
        button = buttonFiller(user, subjectUser, req)
        print(button)
        formactions[req.pk] = button['formaction']
        if button['label']:
            labels[req.pk] = button['label']
        values[req.pk] = button['value']
        receivers[req.pk] = button['receiver']
    for req in incRequests:
        action = req.actions(user)
        actions[req.pk] = action
        if req.position(user) == 1:
            subjectUser = req.user_second
        elif req.position(user) == 2:
            subjectUser = req.user_first
        button = buttonFiller(user, subjectUser, req)
        formactions[req.pk] = button['formaction']
        if button['label']:
            labels[req.pk] = button['label']
        values[req.pk] = button['value']
        receivers[req.pk] = button['receiver']
    return render(request, "friends/friendsbase.html", {'friends': friends, 'incRequests': incRequests, 'sentRequests': sentRequests, 'actions': actions, 'formactions': formactions, 'labels': labels, 'values': values, 'receivers': receivers})

def request_friend(request):
    if request.method == 'POST':
        requester = User.objects.get(pk=request.user.id)
        receiver = User.objects.get(pk=request.POST['receiver'])
        if requester.pk < receiver.pk:
            firstuser = requester
            seconduser = receiver
            type = PENDING_FIRST_SECOND
        elif requester.pk > receiver.pk:
            firstuser = receiver
            seconduser = requester
            type = PENDING_SECOND_FIRST
        newship = Relationship(user_first=firstuser, user_second=seconduser, type=type)
        newship.save()
        return HttpResponseRedirect(reverse('friends-index'))
    else:
        return HttpResponseRedirect(reverse('index'))

def search(request):
    if request.method == 'GET':
        data = request.GET
        query = data['query']
        data = User.objects.filter(username__icontains=query)
        activeUser = User.objects.get(pk=request.user.id)
        # For each result, check for relationship
        results = []
        for result in data:
            try:
                user_first, user_second = orderUsers(activeUser, result)
            except TypeError:
                continue
            try:
                ship = Relationship.objects.filter(user_first=user_first).get(user_second=user_second)
                button = buttonFiller(activeUser, result, ship)
                results.append({'username': result.username, 'pk': result.pk, 'relationship': ship.type, 'button': button})
            except Relationship.DoesNotExist:
                ship = None
                button = {'formaction': reverse('requestfriend'), 'value': 'Request Friend'}
                results.append({'username': result.username, 'pk': result.pk, 'relationship': ship, 'button': button})
        return render(request, 'friends/searchresults.html', {'results': results})
    else:
        return render(request, 'friends/friendsbase.html')

def profile(request, userid):
    user = User.objects.get(pk=userid)
    if user.pk != request.user.id:
        activeUser = User.objects.get(pk=request.user.id)
        # Check if there is a relationship
        shipcheck = checkShip(activeUser, user)
        if shipcheck:
            # Relationship exists, get buttons accordingly
            user_first, user_second = orderUsers(activeUser, user)
            ship = Relationship.objects.get(user_first=user_first, user_second=user_second)
            buttons = buttonFiller(activeUser, user, ship)
        else:
            # No relationship, user should be able to send friend request
            buttons = buttonFiller(activeUser,user,None)
    else:
        buttons = None
    return render(request, 'friends/profile.html', {'user': user, 'lists': user.mylists.all(), 'buttons': buttons})

def accept_friend(request):
    if request.method == 'POST':
        data = request.POST
        activeUser = User.objects.get(pk=request.user.id)
        subjectUser = User.objects.get(pk=data['receiver'])
        user_first, user_second = orderUsers(activeUser, subjectUser)
        shipcheck = checkShip(user_first, user_second)
        if shipcheck:
            ship = Relationship.objects.filter(user_first=user_first).get(user_second=user_second)
            if ship.type == 'PFS' or ship.type == 'PSF':
                ship.type = 'F'
                ship.save()
                print("now friends")
    
                return HttpResponseRedirect(reverse('friends-index'))
            else:
                # Want this to show message to user that they do not have a friend request to accept
                print("no request")
                return HttpResponseRedirect(reverse('index'))
        else:
            # No relationship exists, need to tell user that, give them the option to send friend request
            print("no relationship")
            return HttpResponseRedirect(reverse('index'))
    else:
        # How did you get here?
        print("get request")
        return HttpResponseRedirect(reverse('index'))

def cancel_request(request):
    if request.method == 'POST':
        data = request.POST
        # Check relationship exists
        activeUser = User.objects.get(pk=request.user.id)
        receiver = User.objects.get(pk=data['receiver'])
        user_first, user_second = orderUsers(activeUser, receiver)
        shipcheck = checkShip(user_first, user_second)
        if shipcheck:
            ship = Relationship.objects.get(user_first=user_first, user_second=user_second)
            # Check relationship is a request
            if ship.type == 'PSF' or ship.type == 'PFS':
                ship.delete()
                # Really need to display a success message, this should be a JSON response that displays the succesS
                # wherever the button was on the page
                message = 'Request Deleted'
                return HttpResponseRedirect(reverse('friends-index'))
            else:
                # Can't cancel as there is no request
                # Turn into JSON response
                return HttpResponseRedirect(reverse('index'))
        else:
            # no relationship
            # Turn into JSON repsonse
            return HttpResponseRedirect(reverse('index'))
    else:
        # How did you get here?
        # Turn into JSON response
        return HttpResponseRedirect(reverse('index'))

def remove_friend(request):
    if request.method == "POST":
        data = request.POST
        activeUser = User.objects.get(pk=request.user.id)
        receiver = User.objects.get(pk=data['receiver'])
        user_first, user_second = orderUsers(activeUser, receiver)
        shipcheck = checkShip(user_first, user_second)
        if shipcheck:
            ship = Relationship.objects.get(user_first=user_first, user_second=user_second)
            if ship.type == 'F':
                ship.delete()
                return HttpResponseRedirect(reverse('friends-index'))
            else:
                # Not friends, can't remove
                return HttpResponseRedirect(reverse('friends-index'))
        else:
            # No relationship
            return HttpResponseRedirect(reverse('friends-index'))
    else:
        return HttpResponseRedirect(reverse('friends-index'))

@csrf_exempt
def add_rating(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        user = User.objects.get(pk=request.user.id)
        subject = jsondata.get('subject')
        name = jsondata.get('subjectname')
        rating = jsondata.get('rating')
        subjecttype = jsondata.get('subjecttype')
        # Check if editing review
        if ratingCheck(user, subject):
            oldRating = Rating.objects.filter(user=user).get(subject=subject)
            oldRating.rating = rating
            if jsondata.get('review'):
                review = jsondata.get('review')
                oldRating.review = review
                oldRating.save()
            else:
                oldRating.save()
            response = JsonResponse({'message': 'Rating Updated', 'success': True})
        else:
            if jsondata.get('review'):
                review = jsondata.get('review')
                newRating = Rating(user=user,subject=subject,subjecttype=subjecttype,name=name,rating=rating,review=review)
                newRating.save()
                print("success")
                # logActivity(request, 'Reviewed', newRating, subject)
            else:
                newRating = Rating(user=user,subject=subject,subjecttype=subjecttype,name=name,rating=rating)
                newRating.save()
                print("success")
                # logActivity(request, 'Rated', newRating, subject)
            response = JsonResponse({'message': 'Rating Saved', 'success': True})
        return response

    else:
        return HttpResponseRedirect(reverse('friends-index'))

def activity(request):
    user = User.objects.get(pk=request.user.id)
    # Get user's friend relationships
    friendsquery = Relationship.objects.filter(type=FRIENDS).filter(Q(user_first=user) | Q(user_second=user))
    # Get users from friend relationships
    friendIDS = []
    for ship in friendsquery:
        other = ship.otherUser(user)
        friendIDS.append(other.pk)
    friends = User.objects.filter(pk__in=friendIDS)
    activities = Activity.objects.filter(user__in=friends).order_by('-when')
    serializeddata = [activity.serialize() for activity in activities]
    response = JsonResponse(serializeddata, safe=False)
    return response