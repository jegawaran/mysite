from django.urls import path
from . import views


urlpatterns = [
path('profile',views.conprofile,name='profile'),
path('edit_profile/<int:user_pk>/edit_profile',views.editProfile,name='edit_profile'),
]
