from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('schedule/create/', views.create_schedule, name='create_schedule'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
    path('schedule/<int:schedule_id>/event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
]
