from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title} - {self.starting_bid}"

    @property
    def highest_bid(self):
        return self.bids.order_by('-amount').first()

    @property
    def is_active(self):
        return self.highest_bid is None or self.highest_bid.amount < self.starting_bid


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.amount} - {self.bidder} - {self.listing}"


class Auction(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="auction")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="auctions")
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(timezone.now() + timezone.timedelta(days=30))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction for {self.listing}"


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_by")    

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user} is watching {self.listing}"
