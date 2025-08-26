import requests
from django.conf import settings

def get_tmdb_data(endpoint, params=None):
    base_url = "https://api.themoviedb.org/3"
    image_base_url = "https://image.tmdb.org/t/p/w500"  
    params = params or {}
    params['api_key'] = settings.TMDB_API_KEY
    response = requests.get(f"{base_url}/{endpoint}", params=params)
    data = response.json()
    
    
    if 'results' in data:
        for item in data['results']:
       
            if 'poster_path' in item:
                if item['poster_path'] != None:
                    item['poster_url'] = f"{image_base_url}{item['poster_path']}"

            if 'profile_path' in item:                         
                if item['profile_path'] != None:
                    item['poster_url'] = f"{image_base_url}{item['profile_path']}"
            
    return data