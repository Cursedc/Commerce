from django.contrib import admin
from .models import *


class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','creator','start_bid']
    list_display_links = ['title', 'creator']
    search_fields = ['title', 'content']

admin.site.register(User)
admin.site.register(AuctionListings, AuctionListingsAdmin)
admin.site.register(Comments)
admin.site.register(Bid)
admin.site.register(Category)