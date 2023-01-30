from django.db.models.signals import post_save
from django.dispatch import receiver
from friends.models import Activity
from watching.models import Rating, ListItem, List

# Define actions
RATE = 'rated'
REVIEW = 'reviewed'
LIST = 'added'
WATCH = 'watched'
CREATELIST = 'created'

@receiver(post_save, sender=Rating)
def rating_activity(sender, instance, **kwargs):
    user = instance.user
    rating = instance
    subject = instance.subject
    subjecttype = instance.subjecttype
    if instance.review == '':
        newActivity = Activity(user=user,action=RATE, rating=rating, subject=subject, subjecttype=subjecttype)
    else:
        newActivity = Activity(user=user, action=REVIEW, rating=rating, subject=subject, subjecttype=subjecttype)
    newActivity.save()

@receiver(post_save, sender=ListItem)
def listitem_activity(sender, instance, **kwargs):
    user = instance.list.owner
    item = instance
    subject = instance.itemID
    type = instance.type
    if instance.list.name == 'Watched':
        newActivity = Activity(user=user, action=WATCH, listitem=item, subject=subject, subjecttype=type)
    else:
        newActivity = Activity(user=user,action=LIST, listitem=item, subject=subject, subjecttype=type)
    newActivity.save()

@receiver(post_save, sender=List)
def list_activity(sender, instance, **kwargs):
    user = instance.owner
    item = instance
    newActivity = Activity(user=user, action=CREATELIST, list=item)
    newActivity.save()