"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('watching/', include([
        path('', include('watching.urls')),
        path('community/', include('friends.urls')),
        path('admin/', admin.site.urls),
        path('reset-password', auth_views.PasswordResetView.as_view(), name='password_reset'), # name = 'password_reset', request reset link
        path('reset-password-done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), # name = 'password_reset_done', confirms email sent 
        path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # name = 'password_reset_confirm', for entering new password
        path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete') # name = 'password_reset_complete'
    ])),
]
