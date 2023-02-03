
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('rooms', views.rooms, name='rooms'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('sing-in', views.sing_in, name='sing_in'),
    path('profile', views.profile, name='profile'),
    path('details/<str:name>', views.event_details, name='details'),
    path('add-room', views.add_room, name='add_room'),
    path('delete-room/<str:name>', views.delete_room, name='delete_room'),
    path('add-event', views.add_event, name='add_event'),
    path('cancel-event/<str:name>', views.cancel_event, name='cancel_event'),
    path('cancel_subs/<str:name>', views.cancel_subscription, name='cancel_subscription'),
    path('book-event/<str:name>', views.book_event, name='book_event'),
]
