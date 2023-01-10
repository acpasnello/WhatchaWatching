from django.urls import reverse
from .models import Activity, Relationship

def logActivity(request, media, action):
    newactivity = Activity(user=request.user, action=action, subject=media)
    newactivity.save()
    return True

def orderUsers(user1, user2):
    if user1.pk < user2.pk:
        user_first = user1
        user_second = user2
    elif user1.pk > user2.pk:
        user_first = user2
        user_second = user1
    else:
        return False
    
    return user_first, user_second

def checkShip(user1, user2):
    user_first, user_second = orderUsers(user1, user2)
    shipcheck = Relationship.objects.filter(user_first=user_first).filter(user_second=user_second).count()
    if shipcheck == 1:
        return True
    else:
        return False

def arrangeRequests(userInQuestion):
    # 
    pass

def buttonFiller(activeUser, subjectUser, ship):
    # This helper function will return the necessary info for displaying buttons 
    # concerning the active user's options for interacting with the user in question
    # Give options for friend request, blocking
    # Need to supply button text, form action
    action = ship.actions(activeUser)
    if action == None:
        # Request Friend
        value = 'Send Friend Request'
        formaction = reverse('requestfriend')
        receiver = subjectUser.pk
        # Block
    elif action == 'wait':
        # Wait for response or cancel request
        label = 'Awaiting Response'
        value = 'Cancel Friend Request'
        formaction = reverse('cancelrequest')
        receiver = subjectUser.pk
    elif action == 'respond':
        # Accept or deny friend request
        label = "Respond to Request"
        value = ['Accept', 'Reject']
        formaction = [reverse('acceptfriend'), reverse('cancelrequest')]
        receiver = subjectUser.pk
    elif action == 'remove':
        # Are friends, can remove friend or block
        label = 'Remove Friend'
        value = 'Remove Friend'
        formaction = reverse('removefriend')
        receiver = subjectUser.pk
    elif action == 'unblock':
        # Currently blocked, can unblock
        pass
    else:
        button = None

    
    button = {'value': value, 'formaction': formaction, 'receiver': receiver, 'label': label}
    return button