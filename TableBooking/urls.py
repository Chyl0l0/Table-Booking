from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-room/', views.create_room, name="create-room"),
    path('create-layout/', views.create_layout, name="create-layout"),
    path('create-booking/', views.create_booking, name="create-booking"),
    path('select-table/', views.select_table, name="select-table"),
    path('bookings/', views.UserBookings.as_view(), name='user-bookings'),
    path('today-bookings/', views.TodayBookings.as_view(), name='today-bookings'),

]