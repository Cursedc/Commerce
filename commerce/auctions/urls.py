from django.conf.urls.static import static
from django.urls import path

from commerce import settings
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path("create/", Create.as_view(), name="create"),
    path("specific/<int:pk>", DetailAndFormView.as_view(), name='specific'),
    path('watchlist/<int:listing_id>', watchlist_add, name='watchlist_add'),
    path('my_watchlist/', MyWatchlist, name='my_watchlist'),
    path('cats', categories, name='cat'),
    path('cats/<int:cat_id>', selected_cat, name='cat_selected'),
    path('close/<int:listing_id>', close_listing, name='close_listing'),
    path('make_bid/<int:listing_id>', make_bid, name='make_bid')

]


