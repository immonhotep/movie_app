from django.contrib import admin
from .models import Profile,Watchlist,MovieReview,MovieRating,PersonRating,PersonReview

admin.site.register(Profile)
admin.site.register(Watchlist)
admin.site.register(MovieReview)
admin.site.register(MovieRating)
admin.site.register(PersonRating)
admin.site.register(PersonReview)


