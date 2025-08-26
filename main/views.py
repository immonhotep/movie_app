from django.shortcuts import render,redirect
from django.views.generic import View,DetailView
from .forms import CreateUserForm,UserLoginForm,Userform,ProfileForm,MovieReviewForm,PersonReviewForm,ChangePasswordForm
from .models import Watchlist,MovieReview,MovieRating,PersonReview,PersonRating
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse,reverse_lazy
from .mixins import SuperUserRequiredMixin
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404
from datetime import date
import re
from django.db.models import Q 
from django.conf import settings
import os
import datetime
from django.conf import settings
from .tmdb_api import get_tmdb_data
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg,Count
from itertools import chain

from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text



class AdminPanel(SuperUserRequiredMixin,View):

    def get(self,request):
        return render(request,'main/admin.html')
    

class AdminListMovieReviews(SuperUserRequiredMixin,View):

    def get(self,request):
       
        status = request.GET.get('reviewstatus')

        if status == "on":
            reviews = MovieReview.objects.filter(allowed="True").order_by('-date_updated')
            request.session['checkbox_status'] = "on"
        if status == None:
            reviews = MovieReview.objects.filter(allowed="False").order_by('-date_updated')
            request.session['checkbox_status'] = "off"

              
        p = Paginator(reviews,10)
        page = self.request.GET.get('page')

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages)


        context = {'reviews':reviews,'header':'Movie reviews'}
        return render(request,'main/admin_movie_reviews.html',context)
    

class AdminListPersonReviews(SuperUserRequiredMixin,View):

    def get(self,request):

        status = request.GET.get('reviewstatus')

        if status == "on":
            reviews = PersonReview.objects.filter(allowed="True").order_by('-date_updated')
            request.session['checkbox_status'] = "on"
        if status == None:
            reviews = PersonReview.objects.filter(allowed="False").order_by('-date_updated')
            request.session['checkbox_status'] = "off"

     
        p = Paginator(reviews,10)
        page = self.request.GET.get('page')

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages)


        context = {'reviews':reviews,'header':'Person reviews'}
        return render(request,'main/admin_person_reviews.html',context)
    

class AdminListUsers(SuperUserRequiredMixin,View):

    def get(self,request):

        status = request.GET.get('userstatus')
        
        if status == "on":
            users = User.objects.filter(is_active=True).order_by('-date_joined')
            request.session['user_checkbox'] = "on"
        if status == None:
            users = User.objects.filter(is_active=False).order_by('-date_joined')
            request.session['user_checkbox'] = "off"


        users = users.exclude(pk=1)

        p = Paginator(users,10)
        page = self.request.GET.get('page')

        try:
            users = p.page(page)
        except PageNotAnInteger:
            users = p.page(1)
        except EmptyPage:
            users = p.page(p.num_pages)


        context = {'users':users,'header':'Site Users'}
        return render(request,'main/users.html',context)
    

class ModifyUserStatus(SuperUserRequiredMixin,View):

    def post(self,request,pk):

        user = get_object_or_404(User,pk=pk)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()

        messages.success(request,f'{user} status has been modified')
        return redirect(request.META.get('HTTP_REFERER'))


class UpdateMovieReviewStatus(SuperUserRequiredMixin,View):

    def get(self,request,pk):

        review = get_object_or_404(MovieReview,pk=pk)
        if review.allowed == True:
            review.allowed = False
            review.save()
        else:
            review.allowed = True
            review.save()
        messages.success(request,'review status modified')
        return redirect(request.META.get('HTTP_REFERER'))
    

class UpdatePersonReviewStatus(SuperUserRequiredMixin,View):

    def get(self,request,pk):

        review = get_object_or_404(PersonReview,pk=pk)
        if review.allowed == True:
            review.allowed = False
            review.save()
        else:
            review.allowed = True
            review.save()
        messages.success(request,'review status modified')
        return redirect(request.META.get('HTTP_REFERER'))



class TopRatedView(View):
    def get(self, request):
        movie_data = get_tmdb_data('movie/top_rated', {'language': 'en-US', 'page': 1})
        if 'status_code' in movie_data:
            if movie_data['status_code'] == 7:
                return redirect('error')
            
        movies = movie_data['results']
        
            
        #top 100 movies 
        for page in range(2,5):  
            data =  get_tmdb_data('movie/top_rated', {'language': 'en-US', 'page': page})
            movies.extend(data['results'])

     
        rating_dict = {}
        for movie in movies:
            movie_id = movie['id']
            rating = MovieRating.objects.filter(movie_tmdb_id=movie['id']).aggregate(average=Avg('rate'))
            rating_dict.update({movie_id:rating})
        

        p = Paginator(movies,8)
        page = self.request.GET.get('page')

        try:
            movies = p.page(page)
        except PageNotAnInteger:
            movies = p.page(1)
        except EmptyPage:
            movies = p.page(p.num_pages)

        context = {'movies': movies,'rating_dict':rating_dict,'header':'Top rated'}
        return render(request, 'main/home.html', context)
    



class ShowMovieByGenre(View):

    def get(self,request,genre_id,genre_name):

        movie_data = get_tmdb_data(f'discover/movie?with_genres={genre_id}&sort_by=popularity.desc', {'language': 'en-US', 'page': 1})
        if 'status_code' in movie_data:
            if movie_data['status_code'] == 7:
                return redirect('error')
            
        movies = movie_data['results']

        for page in range(2,5):  
            data =  get_tmdb_data(f'discover/movie?with_genres={genre_id}&sort_by=popularity.desc', {'language': 'en-US', 'page': page})
            movies.extend(data['results'])


        rating_dict = {}
        for movie in movies:
            movie_id = movie['id']
            rating = MovieRating.objects.filter(movie_tmdb_id=movie['id']).aggregate(average=Avg('rate'))
            rating_dict.update({movie_id:rating})

    
        p = Paginator(movies,8)
        page = self.request.GET.get('page')

        try:
            movies = p.page(page)
        except PageNotAnInteger:
            movies = p.page(1)
        except EmptyPage:
            movies = p.page(p.num_pages)

        context = {'movies': movies,'rating_dict':rating_dict,'header':genre_name}
        return render(request, 'main/home.html', context)



class MovieDetail(View):
    def get(self, request, movie_id):

        rating = MovieRating.objects.filter(movie_tmdb_id=movie_id).aggregate(average=Avg('rate'))
        average_rate=0
        if rating["average"] is not None:
            average_rate=round(float(rating["average"]),2)
         
    
        countrate = MovieRating.objects.filter(movie_tmdb_id=movie_id).aggregate(count=Count('id'))
        count=0
        if countrate["count"] is not None:
            count = int(countrate["count"])
   
        
        movie_data = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
        if 'status_code' in movie_data:
            code =  movie_data['status_code']
            if code == 34:
                messages.error(request,'Movie not exist')
                return redirect('home')
                      
            if code == 7:
                return redirect('error')

            
        credit_data = get_tmdb_data(f"movie/{movie_id}/credits", {'language': 'en-US'})
        trailer_data = get_tmdb_data(f"movie/{movie_id}/videos", {'language': 'en-US'})
        videos = trailer_data['results']    
        trailer = {}
        video_keys = []
        for video in videos:
            if 'Trailer' in video['type'] and video['site'] == "YouTube":
                video_keys.append(video['key'])

        if video_keys:
            video_key = video_keys[0]    
            trailer = f'https://www.youtube.com/embed/{video_key}'
        
          
       
        companies = movie_data['production_companies']
        
        genres = movie_data['genres']
        actors = credit_data['cast']
        
        crew = credit_data['crew']

        directors = [member for member in crew if member['job'] == 'Director']
        screenplay = [member for member in crew if member['job'] == 'Screenplay']
        cameramans = [member for member in crew if member["job"] == "Director of Photography"]
        musicans = [member for member in crew if member["job"] == "Original Music Composer"]
        producers = [member for member in crew if member["job"] == "Producer"]
           
        context = {'movie':movie_data,
                   'genres':genres,
                   'actors':actors,
                   'directors':directors,
                   'screenplay':screenplay,
                   'cameramans':cameramans,
                   'musicans':musicans,
                   'producers':producers,
                   'rating':rating,
                   'average_rate':average_rate,
                   'count':count,
                   'trailer':trailer,
                   'companies':companies
                   
                   }
        return render(request, 'main/movie-detail.html', context )


class PopularPersons(View):

    def get(self, request):
        person_data = get_tmdb_data(f"person/popular", {'language': 'en-US','page': 1 })
        if 'status_code' in person_data:
            if person_data['status_code'] == 7:
                return redirect('error')
            
        persons = person_data['results']

        for page in range(2,5):  
            data =  get_tmdb_data('person/popular', {'language': 'en-US', 'page': page})
            persons.extend(data['results'])

        
        rating_dict = {}
        for person in persons:
            person_id = person['id']
            rating = PersonRating.objects.filter(person_tmdb_id=person['id']).aggregate(average=Avg('rate'))
            rating_dict.update({person_id:rating})


        p = Paginator(persons,8)
        page = self.request.GET.get('page')

        try:
            persons = p.page(page)
        except PageNotAnInteger:
            persons = p.page(1)
        except EmptyPage:
            persons = p.page(p.num_pages)

        context = {'persons':persons,'rating_dict':rating_dict}
        return render(request, 'main/persons.html', context)

   

class PersonDetail(View):
    def get(self, request, person_id):

        rating = PersonRating.objects.filter(person_tmdb_id=person_id).aggregate(average=Avg('rate'))
        average_rate=0
        if rating["average"] is not None:
            average_rate=round(float(rating["average"]),2)
         
    
        countrate = PersonRating.objects.filter(person_tmdb_id=person_id).aggregate(count=Count('id'))
        count=0
        if countrate["count"] is not None:
            count = int(countrate["count"])


        person_data = get_tmdb_data(f"person/{person_id}", {'language': 'en-US'})

        # check error code
    
        if 'status_code' in person_data:
            code =  person_data['status_code']
            if code == 34:
                messages.error(request,'Person not exist')
                return redirect('popular_persons')
            if code == 7:
                return redirect('error')
            
        person_film_data = get_tmdb_data(f"person/{person_id}/movie_credits", {'language': 'en-US'})
        casts = person_film_data['cast']


        age = None
        died = False
        if person_data['birthday'] != None:
            birthyear = person_data['birthday'][:4]
            if person_data['deathday'] != None:
                deathyear = person_data['deathday'][:4]
                age = int(deathyear) - int(birthyear)
                died = True
            else:
                current_date = date.today()
                current_year = current_date.year
                age = int(current_year) - int(birthyear)
          

        context = {'person':person_data,'rating':rating,'average_rate':average_rate,'count':count,'died':died,'age':age,'casts':casts}
        return render(request, 'main/person-detail.html', context )


class StaffDetail(View):
    def get(self, request, movie_id):
        credit_data = get_tmdb_data(f"movie/{movie_id}/credits", {'language': 'en-US'})
        if 'status_code' in credit_data:
            code =  credit_data['status_code']
            if code == 34:
                messages.error(request,'Movie review not exist')
                return redirect('home')
            if code == 7:
                return redirect('error')
            
        actors = credit_data['cast']
        crew = credit_data['crew']

        context = {'actors':actors,'crew':crew}
        return render(request,'main/staff_detail.html',context)


class PersonRatingDetail(View):

    def get(self,request,person_id):

        person_rates = PersonRating.objects.filter(person_tmdb_id=person_id).order_by('-rate')
        rating = person_rates.aggregate(average=Avg('rate'))

        p = Paginator(person_rates,10)
        page = self.request.GET.get('page')

        try:
            person_rates = p.page(page)
        except PageNotAnInteger:
            person_rates = p.page(1)
        except EmptyPage:
            person_rates = p.page(p.num_pages)

       
        average_rate=0
        if rating["average"] is not None:
            average_rate=round(float(rating["average"]),2)

        context = {'average_rate':average_rate,'person_rates':person_rates}
        return render(request,'main/person_rate_sum.html',context)
    


class MovieRatingDetail(View):

    def get(self,request,movie_id):

        movie_rates = MovieRating.objects.filter(movie_tmdb_id=movie_id).order_by('-rate')
        rating = movie_rates.aggregate(average=Avg('rate'))

        p = Paginator(movie_rates,10)
        page = self.request.GET.get('page')

        try:
            movie_rates = p.page(page)
        except PageNotAnInteger:
            movie_rates = p.page(1)
        except EmptyPage:
            movie_rates = p.page(p.num_pages)

       
        average_rate=0
        if rating["average"] is not None:
            average_rate=round(float(rating["average"]),2)

        context = {'average_rate':average_rate,'movie_rates':movie_rates}
        return render(request,'main/movie_rate_sum.html',context)



class NowPlayingView(View):

    def get(self, request):
        movie_data = get_tmdb_data('movie/now_playing', {'language': 'en-US', 'page': 1})
        if 'status_code' in movie_data:
            if movie_data['status_code'] == 7:
                return redirect('error')
            
        movies = movie_data['results']

        
        #recent 40 movies 
        for page in range(2,3):  
            data =  get_tmdb_data('movie/now_playing', {'language': 'en-US', 'page': page})
            movies.extend(data['results'])



        rating_list = []
        rating_dict = {}
        for movie in movies:
            movie_id = movie['id']
            rating = MovieRating.objects.filter(movie_tmdb_id=movie['id']).aggregate(average=Avg('rate'))
            rating_list.append(rating)
            rating_dict.update({movie_id:rating})  

            
        p = Paginator(movies,8)
        page = self.request.GET.get('page')

        try:
            movies = p.page(page)
        except PageNotAnInteger:
            movies = p.page(1)
        except EmptyPage:
            movies = p.page(p.num_pages)

        context = {'movies': movies,'rating_dict':rating_dict,'header':'New'}
        return render(request, 'main/home.html', context)
    

class MovieSearchView(View):

    def get(self,request):

        search = request.GET.get('search')
        movie_data = get_tmdb_data(f'search/movie?query={search}', {'language': 'en-US', 'page': 1})
        if 'status_code' in movie_data:
            if movie_data['status_code'] == 7:
                return redirect('error')
        
        movies = movie_data['results']

    
        rating_dict = {}
        for movie in movies:
            movie_id = movie['id']
            rating = MovieRating.objects.filter(movie_tmdb_id=movie['id']).aggregate(average=Avg('rate'))
            rating_dict.update({movie_id:rating})

        p = Paginator(movies,8)
        page = self.request.GET.get('page')

        try:
            movies = p.page(page)
        except PageNotAnInteger:
            movies = p.page(1)
        except EmptyPage:
            movies = p.page(p.num_pages)


        context = {'movies':movies,'rating_dict':rating_dict}
        return render(request,'main/home.html',context)
    


class PersonSearchView(View):

    def get(self,request):

        search = request.GET.get('search')
        person_data = get_tmdb_data(f'search/person?query={search}', {'language': 'en-US', 'page': 1})
        if 'status_code' in person_data:
            if person_data['status_code'] == 7:
                return redirect('error')

        persons = person_data['results']

        rating_dict = {}
        for person in persons:
            person_id = person['id']
            rating = PersonRating.objects.filter(person_tmdb_id=person['id']).aggregate(average=Avg('rate'))
            rating_dict.update({person_id:rating})



        p = Paginator(persons,8)
        page = self.request.GET.get('page')

        try:
            persons = p.page(page)
        except PageNotAnInteger:
            persons = p.page(1)
        except EmptyPage:
            persons = p.page(p.num_pages)


        context = {'persons':persons,'rating_dict':rating_dict}
        return render(request,'main/persons.html',context)
    

class AddToWatchlist(LoginRequiredMixin,View):

    def post(self,request,movie_id):

        movie_data = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
        if 'status_code' in movie_data:
            if movie_data['status_code'] == 7:
                return redirect('error')

        title = movie_data['title']
        if 'poster_path' in movie_data:
            if movie_data != None:
               poster_url =  f"https://image.tmdb.org/t/p/w500/{movie_data['poster_path']}"

        

        movie, created = Watchlist.objects.get_or_create(user=request.user,tmdb_id=movie_id,title=title,poster_url=poster_url)
        if created:
            messages.success(request,'Movie has been added to your watchlist')
        else:
            messages.error(request,'This movie already on your watchlist')
        return redirect(request.META.get('HTTP_REFERER'))



class ViewWatchlist(LoginRequiredMixin,View):

    def get(self,request):

        movies = Watchlist.objects.filter(user=request.user).order_by('-date_added')

    
        p = Paginator(movies,8)
        page = self.request.GET.get('page')

        try:
            movies = p.page(page)
        except PageNotAnInteger:
            movies = p.page(1)
        except EmptyPage:
            movies = p.page(p.num_pages)

        context = {'movies':movies}
        return render(request,'main/watchlist.html',context)
    

class DeleteFromWatchlist(LoginRequiredMixin,View):

    def post(self,request,tmdb_id):

        movie = get_object_or_404(Watchlist,tmdb_id = tmdb_id,user=request.user)
        messages.success(request,f'{movie.title} removed from your watchlist')
        movie.delete()
  
        return redirect('watchlist')
    

class MovieReviews(View):

    def get(self,request,movie_id):

        movie_data = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
        if 'status_code' in movie_data:
            code =  movie_data['status_code']
            if code == 34:
                messages.error(request,'Movie review not exist')
                return redirect('home')
            if code == 7:
                return redirect('error')
            
        title = movie_data['title']
        poster_url = movie_data['poster_path']
     
        
        form = MovieReviewForm()
        reviews = MovieReview.objects.filter(movie_tmdb_id = movie_id).order_by('-date_updated')
        rating = MovieRating.objects.filter(movie_tmdb_id=movie_id)

        current_date = date.today()

        today = datetime.datetime(
        year=current_date.year, 
        month=current_date.month,
        day=current_date.day,
        )
        

        movie_release = movie_data['release_date']
        movie_release = datetime.datetime.strptime(movie_release, '%Y-%m-%d')

        if movie_release < today:
            released = "True"
        else:
            released = "False"


        if request.user.is_authenticated:
            movie_own_rating = rating.filter(user=request.user).first()
        else:
            movie_own_rating = {}

       
        
        p = Paginator(reviews,8)
        page = self.request.GET.get('page')

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages)

        context = {'form':form,'reviews':reviews,'movie_id':movie_id,'title':title,'rating':rating,'movie_own_rating':movie_own_rating,'released':released,'poster_url':poster_url}
        return render(request,'main/movie_reviews.html',context)
    
    @method_decorator(login_required)
    def post(self,request,movie_id):
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_tmdb_id = movie_id
            movie_data = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
            review.title = movie_data['title']
            review.poster_url =  movie_data['poster_path']
            review.user = request.user
            review.save()
            messages.success(request,'Your review saved')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

        return redirect('movie_reviews',movie_id)



class SendMovieRating(LoginRequiredMixin,View):

    def post(self,request,movie_id):

        rate_range = request.POST.get('rate_range')

        if MovieRating.objects.filter(user=request.user,movie_tmdb_id=movie_id).exists():
            messages.error(request,"You already rated this movie")
            return redirect('movie_reviews',movie_id)
        else:

            movie_data = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
            title = movie_data['title']
            poster_url =  movie_data['poster_path']

            MovieRating.objects.create(user=request.user,movie_tmdb_id=movie_id,rate=rate_range,title=title,poster_url=poster_url)
            messages.success(request,'Rating saved')
        
        return redirect('movie_reviews',movie_id)
    

class RemoveMovieReview(LoginRequiredMixin,View):

    def post(self,request,pk):

        review = get_object_or_404(MovieReview,pk=pk)
        if review.user == request.user or request.user.is_superuser:
            review.delete()
            messages.success(request,'Movie review removed')
            
        return redirect(request.META.get('HTTP_REFERER'))
    
class EditMovieReview(LoginRequiredMixin,View):

    def get(self,request,pk):
        review = get_object_or_404(MovieReview,pk=pk)
        if review.user == request.user:
            form = MovieReviewForm(instance=review)
            context = {'form':form,'header':'Edit review'}
            return render(request,'main/site_forms.html',context)
        
    def post(self,request,pk):

        review = get_object_or_404(MovieReview,pk=pk)
        if review.user == request.user:
            form = MovieReviewForm(request.POST,instance=review)
            if form.is_valid():
                form.save()
                messages.success(request,'review edited')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)


            return redirect('movie_reviews',review.movie_tmdb_id)


class ResetMovieRating(LoginRequiredMixin,View):

    def get(self,request,pk):

        rating = get_object_or_404(MovieRating,pk=pk,user=request.user)
        rating.delete()
        messages.success(request,'Your rating has been resetet, now you can rate again')
        return redirect(request.META.get('HTTP_REFERER'))
        



class RemovePersonReview(LoginRequiredMixin,View):

    def post(self,request,pk):

        review = get_object_or_404(PersonReview,pk=pk)
        if review.user == request.user or request.user.is_superuser:
            review.delete()
            messages.success(request,'Person review removed')

        return redirect(request.META.get('HTTP_REFERER'))   
        
    
    
class EditPersonReview(LoginRequiredMixin,View):

    def get(self,request,pk):
        review = get_object_or_404(PersonReview,pk=pk)
        if review.user == request.user:
            form = PersonReviewForm(instance=review)
            context = {'form':form,'header':'Edit review'}
            return render(request,'main/site_forms.html',context)
        
    def post(self,request,pk):

        review = get_object_or_404(PersonReview,pk=pk)
        if review.user == request.user:
            form = PersonReviewForm(request.POST,instance=review)
            if form.is_valid():
                form.save()
                messages.success(request,'review edited')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)


            return redirect('person_reviews',review.person_tmdb_id)



class PersonReviews(View):

    def get(self,request,person_id):

        person_data = get_tmdb_data(f"person/{person_id}", {'language': 'en-US'})
        if 'status_code' in person_data:
            code =  person_data['status_code']
            if code == 34:
                messages.error(request,'Person review not exist')
                return redirect('popular_persons')
            if code == 7:
                return redirect('popular_persons')


        name = person_data['name']
        profile_path = person_data['profile_path']

        form = PersonReviewForm()
        reviews = PersonReview.objects.filter(person_tmdb_id = person_id).order_by('-date_updated')
        rating = PersonRating.objects.filter(person_tmdb_id=person_id)

        if request.user.is_authenticated:
            person_own_rating = rating.filter(user=request.user).first()
        else:
            person_own_rating = {}
     
        
        p = Paginator(reviews,8)
        page = self.request.GET.get('page')

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages)

        context = {'form':form,'reviews':reviews,'person_id':person_id,'name':name,'rating':rating,'person_own_rating':person_own_rating,'profile_path':profile_path}
        return render(request,'main/person_reviews.html',context)
    
    @method_decorator(login_required)
    def post(self,request,person_id):
        form = PersonReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.person_tmdb_id = person_id
            person_data = get_tmdb_data(f"person/{person_id}", {'language': 'en-US'})
            review.name = person_data['name']
            review.poster_url = person_data['profile_path']
            review.user = request.user
            review.save()
            messages.success(request,'Your review saved')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

        return redirect('person_reviews',person_id)


class ResetPersonRating(LoginRequiredMixin,View):

    def get(self,request,pk):

        rating = get_object_or_404(PersonRating,pk=pk,user=request.user)
        rating.delete()
        messages.success(request,'Your rating has been resetet, now you can rate again')
        return redirect(request.META.get('HTTP_REFERER'))



class UserStatistic(View):

    def get(self,request,pk):

        user = get_object_or_404(User,pk=pk)

        movie_rate = MovieRating.objects.filter(user=user)
        person_rate = PersonRating.objects.filter(user=user)

        movie_rate_count = movie_rate.count()
        person_rate_count = person_rate.count()

        movie_ratings = movie_rate.order_by('-date_updated')[:8]
        person_ratings = person_rate.order_by('-date_updated')[:8]

        movie_reviews = MovieReview.objects.filter(user=user).order_by('-date_updated')
        person_reviews = PersonReview.objects.filter(user=user).order_by('-date_updated')

        #union movie and person ratings with chain
        all_ratings = list(chain(movie_reviews,person_reviews))

        p = Paginator(all_ratings,8)
        page = self.request.GET.get('page')

        try:
            all_ratings = p.page(page)
        except PageNotAnInteger:
            all_ratings = p.page(1)
        except EmptyPage:
            all_ratings = p.page(p.num_pages)



        
        context = {
            'movie_reviews':movie_reviews,
            'person_reviews':person_reviews,
            'movie_ratings':movie_ratings,
            'person_ratings':person_ratings,
            'user':user,
            'movie_rate_count':movie_rate_count,
            'person_rate_count':person_rate_count,
            'all_ratings':all_ratings,
            
            }
        return render(request,'main/statistic.html',context)



class UserMovieRatings(View):

  def get(self,request,pk):
    user = get_object_or_404(User,pk=pk)
    movie_rates = MovieRating.objects.filter(user=user).order_by('-date_updated')
    

    p = Paginator(movie_rates,8)
    page = self.request.GET.get('page')

    try:
        movie_rates = p.page(page)
    except PageNotAnInteger:
        movie_rates = p.page(1)
    except EmptyPage:
        movie_rates = p.page(p.num_pages)
    
    context = {'movie_rates':movie_rates,'user':user}
    return render(request,'main/movie_rates.html',context)



class UserPersonRatings(View):

  def get(self,request,pk):
    user = get_object_or_404(User,pk=pk)
    person_rates = PersonRating.objects.filter(user=user).order_by('-date_updated')
    

    p = Paginator(person_rates,8)
    page = self.request.GET.get('page')

    try:
        person_rates = p.page(page)
    except PageNotAnInteger:
        person_rates = p.page(1)
    except EmptyPage:
        person_rates = p.page(p.num_pages)
    
    context = {'person_rates':person_rates,'user':user}
    return render(request,'main/person_rates.html',context)

      
      


class ChangePassword(LoginRequiredMixin,View):

    def get(self,request):
        form = ChangePasswordForm(user=request.user)
        context = {'form':form,'header':'Change your password'}
        return render(request,'main/site_forms.html',context)

    def post(self,request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,request.user)
            messages.success(request,'Your password has been changed')   
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
            return redirect('change_password')
        return redirect('edit_profile')   



class SendPersonRating(LoginRequiredMixin,View):

    def post(self,request,person_id):

        rate_range = request.POST.get('rate_range')
        if PersonRating.objects.filter(user=request.user,person_tmdb_id=person_id).exists():
            messages.error(request,"You already rated this person")
            return redirect('person_reviews',person_id)
        else:
            person_data = get_tmdb_data(f"person/{person_id}", {'language': 'en-US'})
            name = person_data['name']
            poster_url =  person_data['profile_path']
            PersonRating.objects.create(user=request.user,person_tmdb_id=person_id,rate=rate_range,name=name,poster_url=poster_url)
            messages.success(request,'Rating saved')
        
        return redirect('person_reviews',person_id)
    
   

class RegistrationView(View):

    def get(self,request):

        if request.user.is_authenticated:
            return redirect('home')

        form = CreateUserForm()
        context = {'form':form,'header':'Registration'}
        return render(request,'main/auth_forms.html',context)

    def post(self,request):

        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        

            current_site = get_current_site(self.request)

            subject = 'Activate Your Account'
            message = render_to_string('settings/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),})
           
            try:
                user.email_user(subject=subject, message=message)              
                messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
                return redirect('user_register')
            except:
                messages.error(self.request,'Mail Server Connection problem, please turn to website admin')




        else:
            for key, error in list(form.errors.items()):
                messages.error(request, error)
            return redirect('user_register')
        
        return redirect('user_login')
    

def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)    
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('user_login')

    else:
        return render(request, 'settings/activation_invalid.html')
    

class UserLoginView(View):

    def get(self,request):

        if request.user.is_authenticated:
            return redirect('home')

        form = UserLoginForm()
        context = {'form':form,'header':'Login'}
        return render(request,'main/auth_forms.html',context)
    
    def post(self,request):

        form = UserLoginForm(data=request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username,password=password)
            if user is not None:
                messages.success(request,f'welcome {user}') 
                login(request,user)
                
        else:
            messages.error(request,'Invalid username or password')
            return redirect('user_register')
        
        return redirect('home')


class UserLogoutView(View):

    def post(self,request):
        messages.error(request,'Bye bye')
        logout(request)
        return redirect('home')


class ProfileEdit(LoginRequiredMixin,View):

    def get(self,request):

        userform = Userform(instance=request.user)
        profileform = ProfileForm(instance=request.user.profile)
        context = {'userform':userform,'profileform':profileform,'header':'Edit Profile'}
        return render(request,'main/edit_profile.html',context)
    
    def post(self,request):

        userform = Userform(request.POST,request.FILES,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=request.user.profile)

        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,'Your profile updated')
            return redirect('home')
        else:
            for error in list(userform.errors.values()):
                messages.error(request, error)

            for error in list(profileform.errors.values()):
                messages.error(request, error)
            return redirect('edit_profile')


        

class ErrorPage(View):

    def get(self,request):
        return render(request,'main/error.html')





    






