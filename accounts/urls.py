from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
#    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('registration/', views.registation_user, name='user_registration'),
    path('registration_done/', views.registration_complete, name='user_registration_complete'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile_change/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile_follow/<int:pk>/', views.users_follow, name='profile_follow'),
    path('follow_list/<int:pk>/<int:flag>', views.FollowListView.as_view(), name='follow_list')
]