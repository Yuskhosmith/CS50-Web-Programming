from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createlisting", views.createlisting, name="createlisting"),
    path('listing/', views.index, name='index'),
    path('listing/<int:listing_id>', views.listing, name='listing_by_id'),
    path('bid/<int:listing_id>', views.bid, name='bid'),
    path('comment/<int:listing_id>', views.comment, name='comment'),
    path('category/<str:category>', views.category, name='category'),
]
