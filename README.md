# Movie information & recomendation system

Application backend : Python/Django

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,django,djangorestframework"
    />
  </a>
</p>

Application Frontend: Html, Bootsrap css, Custom css, and Javascripts

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=html,bootstrap,css,javascript"
    />
  </a>
</p>


Description:


- TMDB API powered movie information & recommendation system with feature of leave comments,create ratings and add movies to own watchlist.


Application reason & usage:

- This application strictly planed to use to personal, educational reason, and github showcase. never planed to go in production.
- Application only allowed to use in personal, educational, non commerical purposes.


IMPORTANT:

- This product uses the TMDB API but is not endorsed or certified by TMDB

- The application fetches movie, and person information from TMDB api datasets, this way valid API key required for the usage. Without api key the 
  application not working.
  
- API key not included to the application. 
- TMDB API key is free for only non commerical purposes for developers 


1. To get your own free api key please visit: https://www.themoviedb.org/settings/api for the details.

2. After you get your personal api key, clone this repository, and find the main configuration file: movie_app/settings.py.

3. Need locate the constans: TMDB_API_KEY in the settings.py file, and replace the 'PLACE_YOUR_TMDB_API_KEY_HERE' value with your api key.



FUNCTIONS:

1. Authentication & account : 
 - User login and register (with email confirmation)
 - Modify user account
 - Reset Password 

2. Show New movies:
 - Application fetch popular 40 new movies from api witch currently running on movies or streaming platforms.

3. Show Top rated movies:
  - Application fetch top 100 tmdb rated movies from api

4. Show Movie detail:
 - Application fetch movie important details from api, including actors, staff information, and trailer with youtube embed url

5. Show Top Persons:
  - Application fetch top 100 tmdb popular persons from api

6. Show person detail:
 - Application fetch detailed person information from api.

7. Watchlist:
  - Show personal watchlist with movies for authenticated users
  - Movies can be added to signed in users personal watchlists.
  - Signed in users can remove movies from own watchlist.

8. Rating and review about movies:
  - Signed in users can send movie rating with (0-100) percentage based range slider, also can send reviews about movies.
  - Signed in user can modify and delete own reviews.
  - Signed in users can reset own ratings.

9. Rating and review about persons:
  - Signed in users can send person rating with (0-100) percentage based range slider, also can send reviews about persons.
  - Signed in user can modify and delete own reviews.
  - Signed in users can reset own ratings.

10. Search Functions for movies and persons:
  - Api based search functions to find people by name, and find movie by title.

11. Other features
- Fetch genres list, and movies by genres from api.
- Paginator function on all major pages implemented.
- User Statistic to list rated, and reviewed movies and persons

12. Admin Functions
- List movie reviews, hide/unhide reviews, delete reviews
- List person reviews, hide/unhide reviews, delete reviews
- List users, activate or deactivate users 


INSTALLED MODULES:

- aiosmtpd==1.4.6
- annotated-types==0.7.0
- asgiref==3.9.0
- atpublic==6.0.1
- attrs==25.3.0
- beautifulsoup4==4.13.4
- certifi==2025.7.9
- charset-normalizer==3.4.2
- crispy-bootstrap5==2025.6
- Django==4.2.23
- django-bootstrap-datepicker-plus==5.0.5
- django-bootstrap-v5==1.0.11
- django-crispy-forms==2.4
- django-resized==1.0.3
- django-tinymce==4.1.0
- fontawesomefree==6.6.0
- idna==3.10
- pillow==11.3.0
- pydantic==2.11.7
- pydantic_core==2.33.2
- PyJWT==2.9.0
- python-dateutil==2.9.0.post0
- pytz==2025.2
- requests==2.32.4
- six==1.17.0
- soupsieve==2.7
- sqlparse==0.5.3
- typing-inspection==0.4.1
- typing_extensions==4.14.1
- tzdata==2025.2
- urllib3==2.5.0


NOTES:

SENDING MAILS:

This site use email validated registration.
For the usage need some kind of mail server at least for the testing, or need modify the settings.py to real email providers port, and credentials

very simple pre-installed method for tesing with fake mail server on localhost port 1025:

aiosmtpd version 1.4.6 installed within the virtual environment with the requirements.txt, so just run in a different terminal (in the same virtual environment) the following command to run fake mailserver:

python -m aiosmtpd -n -l localhost:1025

emails will appear in the terminal




INSTALL:

- clone the repository ( git clone https://github.com/immonhotep/movie_app.git )
- Create python virtual environment and activate it ( depends on op system, example on linux: virtualenv venv  and source venv/bin/activate )
- Install the necessary packages and django  ( pip3 install -r requirements.txt ) into the virtual environment
- Make sure about your own tmdb api key properly configured on settings.py
- Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
- Create a superuser ( python3 manage.py createsuperuser )
- Run the application ( python3 manage.py runserver )



Other Info

TMDB api can change over time, this way the api queries have possibity that not work together with api properly in the future.


Showcase images:
Top rated page

![Top rated](https://github.com/user-attachments/assets/320cb871-ec60-47cf-a0c5-07e3b3c90e65)

User Reviews and Rating details
![reviews_and_rating_detail](https://github.com/user-attachments/assets/0789d5d4-4467-4582-beeb-029188fa9979)
