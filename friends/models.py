from django.db import models
from watching.models import User, Media, Rating, ListItem, List
from django.urls import reverse
from datetime import datetime

# Create your models here.
class Relationship(models.Model):
    PENDING_FIRST_SECOND = 'PFS'
    PENDING_SECOND_FIRST = 'PSF'
    FRIENDS = 'F'
    BLOCK_FIRST_SECOND = 'BFS'
    BLOCK_SECOND_FIRST = 'BSF'
    BLOCK_BOTH = 'BB'
    relationship_types = [
        (PENDING_FIRST_SECOND, 'Pending'), # pending_first_second
        (PENDING_SECOND_FIRST, 'Pending'), # pending_second_first
        (FRIENDS, 'Friends'), # friends
        (BLOCK_FIRST_SECOND, 'Blocked'), # block_first_second
        (BLOCK_SECOND_FIRST, 'Blocked'), # block_second_first
        (BLOCK_BOTH, 'Blocked') # block_both
    ]
    # Ensure user_first_id < user_second_id

    user_first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myRelationships1')
    user_second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myRelationships2')
    type = models.CharField(max_length=40, choices=relationship_types)
    created = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)

    # Define method for getting user's position in relationship for using instance
    def position(self, userInQuestion):
        if userInQuestion == self.user_first:
            position = 1
        elif userInQuestion == self.user_second:
            position = 2
        else:
            position = 0
        
        return position

    # Define possible actions 
    def actions(self, userInQuestion):
        position = self.position(userInQuestion)
        
        if position == 1:
            if self.type == 'PFS':
                action = 'wait'
            elif self.type == 'PSF':
                action = 'respond'
            elif self.type == 'F':
                action = 'remove'
            elif self.type == 'BFS':
                action = 'unblock'
            elif self.type == 'BSF':
                action = None
            elif self.type == 'BB':
                action = "unblock"
            return action
        elif position == 2:
            if self.type == 'PFS':
                action = 'respond'
            elif self.type == 'PSF':
                action = 'wait'
            elif self.type == 'F':
                action = 'remove'
            elif self.type == 'BFS':
                action = None
            elif self.type == 'BSF':
                action = 'unblock'
            elif self.type == 'BB':
                action = "unblock"
            return action
        else:
            return None
        
    def otherUser(self, activeUser):
        position = self.position(activeUser)
        if position == 1:
            other = User.objects.get(pk=self.user_second.id)
        elif position == 2:
            other = User.objects.get(pk=self.user_first.id)
        else:
            other = None
        return other

        # https://stackoverflow.com/questions/379236/database-design-best-table-structure-for-capturing-the-user-friend-relationship


class Activity(models.Model):
    # Define actions
    RATE = 'rated'
    REVIEW = 'reviewed'
    LIST = 'added'
    WATCH = 'watched'
    CREATELIST = 'created'
    action_types = [
        (RATE, 'Rated'),
        (REVIEW,'Reviewed'),
        (LIST,'Add to List'),
        (WATCH, 'Watched'),
        (CREATELIST, 'Create new list'),
    ]

    MOVIE = 'M'
    SHOW = 'S'
    media_types = [
    (MOVIE, 'Movie'),
    (SHOW, 'Show'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myActivity')
    action = models.CharField(max_length=30, choices=action_types)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True)
    listitem = models.ForeignKey(ListItem, on_delete=models.CASCADE, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    subject = models.IntegerField(null=True)
    subjecttype = models.CharField(max_length=20, choices=media_types, null=True)
    when = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        if self.rating:
            return {
                'id': self.pk,
                'user': self.user.username,
                'userID': self.user.pk,
                'action': self.action,
                'rating': self.rating.rating,
                'review': self.rating.review,
                'name': self.rating.name,
                'medialink': reverse('details', args=[self.subjecttype, self.subject]),
                'when': self.when.strftime("%d/%m/%Y %I:%M%p")
            }
        elif self.listitem:
            return {
                'id': self.pk,
                'user': self.user.username,
                'userID': self.user.pk,
                'action': self.action,
                'listitem': self.listitem.name,
                'list': self.listitem.list.name,
                'subject': self.subject,
                'when': self.when.strftime("%d/%m/%Y %I:%M%p"),
                'listlink': reverse('viewlist', args=[self.user.pk, self.listitem.list.name]),
                'medialink': reverse('details', args=[self.subjecttype, self.subject])
            }
        elif self.list:
            return {
                'id': self.pk,
                'user': self.user.username,
                'userID': self.user.pk,
                'action': self.action,
                'list': self.list.name,
                'when': self.when.strftime("%d/%m/%Y %I:%M%p"),
                'link': reverse('viewlist', args=[self.user.pk, self.list.name])
            }

    def __str__(self):
        string = ''
        if self.rating:
            string = 'Activity %i: %s rated %s' % (self.pk, self.user.username, self.rating.name)
        elif self.listitem:
            string = 'Activity %i: %s added %s to a list' % (self.pk, self.user.username, self.listitem.name)
        elif self.list:
            string = 'Activity %i: %s created a new list, %s' % (self.pk, self.user.username, self.list.name)
        return string
    