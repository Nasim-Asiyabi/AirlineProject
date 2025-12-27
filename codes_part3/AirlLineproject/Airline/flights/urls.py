from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('cancel/<int:reservation_id>/', views.cancel_flight, name='cancel_flight'),
]