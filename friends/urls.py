from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='friends-index'),
    path('search', views.search, name='friends-search'),
    path('profile/<int:userid>', views.profile, name='profile'),
    path('requestfriend', views.request_friend, name='requestfriend'),
    path('acceptfriend', views.accept_friend, name='acceptfriend'),
    path('cancelrequest', views.cancel_request, name='cancelrequest'),
    path('removefriend', views.remove_friend, name='removefriend'),
    path('addrating', views.add_rating, name='addrating')
]