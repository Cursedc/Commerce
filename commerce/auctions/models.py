from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from commerce import settings

class User(AbstractUser):
    pass


class AuctionListings(models.Model):# объявления об аукционе
    creator = models.ForeignKey('User', on_delete=models.CASCADE, default=None, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, db_index=True, blank=True)
    start_bid = models.FloatField(default=None)

    class Meta:
        verbose_name_plural = 'AuctionListings'

    def get_absolute_url(self):
        return reverse('specific', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Bid(models.Model):# Ставки на аукционе
    bet_user = models.ForeignKey('User', on_delete=models.PROTECT, db_index=True)
    amount = models.FloatField()
    listing = models.ForeignKey('AuctionListings', on_delete=models.CASCADE, default=None)


class Comments(models.Model):# комментарии к объявлениям на ауционе
    commentator = models.ForeignKey('User', on_delete=models.PROTECT, db_index=True)
    comment = models.TextField()
    listing = models.ForeignKey('AuctionListings', on_delete=models.CASCADE, default=None)



    class Meta:
        verbose_name_plural = 'Comments'
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ManyToManyField('AuctionListings', related_name='lists')

    def __str__(self):
        return f"{self.user}'s WatchList"


