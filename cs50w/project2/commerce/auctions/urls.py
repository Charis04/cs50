from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path(
        "remove_from_watchlist/<int:listing_id>",
        views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("open_auction/<int:listing_id>", views.open_auction, name="open_auction"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("categories", views.categories, name="categories"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
