from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('browse', views.browse, name='browse'),
    path('about', views.about, name='about'),
    path('list', views.createlist, name='createlist'),
    path('editlist/<str:name>', views.editlist, name='editlist'),
    path('list/<int:userid>/<str:name>', views.viewlist, name='viewlist'),
    path('mylists', views.mylists, name='mylists'),
    path('search', views.search, name='search'),
    path('details/<str:type>/<int:id>', views.details, name='details'),
    path('addtolist', views.addtolist, name='addtolist'),
    path('removefromlist', views.removefromlist, name='removefromlist'),
    path('getposterpath', views.getposterpath, name='getposterpath'),
]
