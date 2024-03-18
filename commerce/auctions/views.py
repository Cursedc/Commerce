from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from commerce import settings
from .models import *
from .forms import *



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



class Create(CreateView):
    form_class = CreateListing
    template_name = "auctions/create.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class Home(ListView):
    model = AuctionListings
    template_name = "auctions/index.html"
    context_object_name = 'context'

    def get_queryset(self):
        return AuctionListings.objects.all().select_related('cat')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bid'] = Bid.objects.get(listing=c).amount

class Specific(DetailView):
    model = AuctionListings
    template_name = "auctions/specific.html"
    context_object_name = 'context'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.kwargs['pk']
        if Bid.objects.filter(listing=c).exists():
            context['bid'] = Bid.objects.get(listing=c).amount

        if self.request.user.is_authenticated:
            context['b'] = Watchlist.objects.filter(user=self.request.user, item=c).exists()
            context['is_creator'] = (self.request.user == AuctionListings.objects.get(pk=c).creator)
        context['coms'] = Comments.objects.filter(listing=c)
        context['form'] = AddComment()
        return context

class InterestFormView(SingleObjectMixin, FormView): 
    template_name = "auctions/specific.html"
    form_class = AddComment
    model = AuctionListings

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("specific", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.commentator = self.request.user
        form.instance.listing = AuctionListings.objects.get(pk=self.object.pk)
        form.save()
        return super().form_valid(form)
class DetailAndFormView(View):
    def get(self, request, *args, **kwargs):
        view = Specific.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = InterestFormView.as_view()
        return view(request, *args, **kwargs)


def watchlist_add(request, listing_id):
    # Get the user watchlist or create it if it doesn't exists
    item_to_save = get_object_or_404(AuctionListings, pk=listing_id)
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    if Watchlist.objects.filter(user=request.user, item=listing_id).exists():
        user_list.item.remove(item_to_save)
        return HttpResponseRedirect(reverse("specific", args=(listing_id,)))

    # Add the item through the ManyToManyField (Watchlist => item)
    else:
        user_list.item.add(item_to_save)
        return redirect("index")




def MyWatchlist(request):
    curlist = get_object_or_404(Watchlist, user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': curlist})

def categories(request):

    return render(request, 'auctions/cats.html', {'cats': Category.objects.all()})

def selected_cat(request, cat_id):
    c = AuctionListings.objects.filter(cat_id=cat_id).select_related('cat')
    return render(request, 'auctions/index.html', {'context': c})


def close_listing(request, listing_id):
    AuctionListings.objects.filter(pk=listing_id).delete()
    return redirect('index')


def make_bid(request, listing_id):
    if request.method == 'POST':
        amount = float(request.POST['amount'])

        c = list(Bid.objects.filter(listing__id=listing_id))
        if len(c) != 0:
            if amount <= c[0].amount:
                message = 'Amount is too low'
                form = AddBid(request.POST)
                return render(request, 'auctions/make_bid.html', {'form': form, 'messages': message})

        if amount <= AuctionListings.objects.get(pk=listing_id).start_bid:
            message = 'Amount is too low'
            form = AddBid(request.POST)
            return render(request, 'auctions/make_bid.html', {'form': form, 'messages': message})

        if len(c) != 0:
            Bid.objects.get(listing__id=listing_id).delete()
        Bid.objects.create(amount=amount, bet_user=request.user, listing=AuctionListings.objects.get(pk=listing_id))
        return redirect('specific', listing_id)

    form = AddBid()
    return render(request, 'auctions/make_bid.html', {'form': form})