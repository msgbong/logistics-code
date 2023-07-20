from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dash/', views.dash, name='dash'),
    path('sign/', views.sign, name='sign'),
    path('login/', views.login, name='login'),
    path('create_requisition/', views.create_requisition, name='create_requisition'),
    path('review_requisition/<int:requisition_id>/', views.review_requisition, name='review_requisition'),
    path('review_requisition', views.review_requisition, name='review_requisition'),
]
