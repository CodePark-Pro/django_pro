from django.urls import path

from . import views

app_name = 'post_app'

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    #path('post_create/', views.post_create, name='post_create'),
    #クラスビューに変更したので、a_view()でビューをコールする 
    path('', views.PostListView.as_view(), name='post_list'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]