from django.urls import path
from .views import *
from . import views



urlpatterns = [


path('',NowPlayingView.as_view(),name='home'),
path('popular-movies/',TopRatedView.as_view(),name='popular_movies'),
path('movies_by_genre/<int:genre_id>/<str:genre_name>/',ShowMovieByGenre.as_view(),name='movies_by_genre'),
path('search-movie/',MovieSearchView.as_view(),name='movie_search'),
path('search-person/',PersonSearchView.as_view(),name='person_search'),
path('popular-persons/',PopularPersons.as_view(),name='popular_persons'),
path('login/',UserLoginView.as_view(),name='user_login'),
path('logout/',UserLogoutView.as_view(),name='user_logout'),
path('register/',RegistrationView.as_view(),name='user_register'),
path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),
path('change-password/',ChangePassword.as_view(),name='change_password'),
path('edit-profile/',ProfileEdit.as_view(),name='edit_profile'),

path('movie-detail/<int:movie_id>/',MovieDetail.as_view(),name='movie_detail'),
path('person-detail/<int:person_id>/',PersonDetail.as_view(),name='person_detail'),
path('staff_detail/<int:movie_id>/',StaffDetail.as_view(),name='staff_details'),

path('add-to-watchlist/<int:movie_id>/',AddToWatchlist.as_view(),name='add_to_watchlist'),
path('watchlist/',ViewWatchlist.as_view(),name='watchlist'),
path('remove_movie/<int:tmdb_id>/',DeleteFromWatchlist.as_view(),name='remove_movie'),

path('movie-reviews/<int:movie_id>/',MovieReviews.as_view(),name='movie_reviews'),
path("send-movie-rating/<int:movie_id>/",SendMovieRating.as_view(),name="rate_movie"),
path('reset-movie-rating/<int:pk>/',ResetMovieRating.as_view(),name='reset-movie-rating'),
path('person-reviews/<int:person_id>/',PersonReviews.as_view(),name='person_reviews'),
path("send-person-rating/<int:person_id>/",SendPersonRating.as_view(),name="rate_person"),
path('reset-person-rating/<int:pk>/',ResetPersonRating.as_view(),name='reset-person-rating'),
path('person-rate-summary/<int:person_id>/',PersonRatingDetail.as_view(),name='person_rate_summary'),
path('movie-rate-summary/<int:movie_id>/',MovieRatingDetail.as_view(),name='movie_rate_summary'),
path('user-movie-ratings/<int:pk>/',UserMovieRatings.as_view(),name='user_movie_ratings'),
path('user-person-rating/<int:pk>/',UserPersonRatings.as_view(),name='user_person_rating'),

path('edit-movie-review/<int:pk>/',EditMovieReview.as_view(),name='edit_movie_review'),
path('remove-movie-review/<int:pk>/',RemoveMovieReview.as_view(),name='remove_movie_review'),


path('edit-person-review/<int:pk>/',EditPersonReview.as_view(),name='edit_person_review'),
path('remove-person-review/<int:pk>/',RemovePersonReview.as_view(),name='remove_person_review'),

path('statistic/<int:pk>/',UserStatistic.as_view(),name='statistic'),

path('admin-panel/',AdminPanel.as_view(),name='admin_panel'),
path('admin-list-movie-reviews/',AdminListMovieReviews.as_view(),name='admin-list-movie-reviews'),
path('admin-list-person-review/',AdminListPersonReviews.as_view(),name='admin_list_person_reviews'),
path('update-movie-review-status/<int:pk>/',UpdateMovieReviewStatus.as_view(),name='update_movie_review_status'),
path('update-person-review-status/<int:pk>/',UpdatePersonReviewStatus.as_view(),name='update_person_review_status'),
path('list-users/',AdminListUsers.as_view(),name='list_users'),
path('update-user-status/<int:pk>/',ModifyUserStatus.as_view(),name='update_user_status'),
path('error/',ErrorPage.as_view(),name='error'),


]


