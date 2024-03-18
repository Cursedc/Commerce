from django import forms
from .models import *


class CreateListing(forms.ModelForm):

    class Meta:
        model = AuctionListings
        fields = ['title',  'content', 'photo',  'cat', 'start_bid']



class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment', ]


class AddBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', ]