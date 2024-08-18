from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("active", views.active_listings, name="active_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_auction/<int:listing_id>",
         views.close_auction, name="close_auction"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>",
         views.show_categories, name="show_categories"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist/<int:listing_id>",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("remove/<int:listing_id>", views.remove_from_watchlist, name="remove"),
    path("listings/<int:listing_id>", views.listing, name="listing")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
