from .tmdb_api import get_tmdb_data
from .models import MovieRating
from django.db.models import Avg,Count



def navbar_context(request):

    genre_data = get_tmdb_data('genre/movie/list', {'language': 'en-US', 'page': 1})
    if 'status_code' in genre_data:
            if genre_data['status_code'] == 7:
                genre_list = {}
                return {'genre_list':genre_list}
                  
   
    genre_list = genre_data['genres']
    return {'genre_list':genre_list}

    