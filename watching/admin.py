from django.contrib import admin
from watching.models import User, List, ListItem
from friends.models import Relationship

# Register your models here.
admin.site.register(User)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Relationship)