from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="Create Listing"),
    path("listings/<int:item_id>", views.listing_page, name="listing_page"),
    path("watchlist/<int:item_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("categories", views.categories_list, name="categories_list"),
    path("categories/<str:category_title>", views.category, name="category")
]
