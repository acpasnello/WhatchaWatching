from django.contrib import admin
from watching.models import User, List, ListItem, Rating
from friends.models import Relationship, Activity

class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ('when',)

# Register your models here.
admin.site.register(User)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Relationship)
admin.site.register(Rating)
admin.site.register(Activity, ActivityAdmin)

# Correct 'View Site' Link
admin.site.site_url = '/watching'