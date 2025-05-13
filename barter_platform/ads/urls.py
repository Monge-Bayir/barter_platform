from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.list_ads, name='list_ads'),
    path('ads/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    path('ads/<int:pk>/proposal/', views.create_proposal, name='create_proposal'),
    path('proposals/', views.proposals_list, name='proposals_list'),
]