# Generated by Django 4.2.5 on 2023-09-25 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bet_user',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='commentator',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='item',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='AuctionListings',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
