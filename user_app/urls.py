from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='profile'),
    path('search/', views.search_trains, name='search_trains'),
    path('availability/', views.check_availability, name='check_availability'),
    path('book/<int:train_id>/', views.book_train, name='book_train'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]