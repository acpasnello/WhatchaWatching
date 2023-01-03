from django.db import models
from watching.models import User, Media

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
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # action
    # subject = models.ForeignKey(Media, on_delete=models.CASCADE)
    pass