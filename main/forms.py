from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile,MovieReview,PersonReview

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,HTML

from django.contrib.auth.forms import PasswordChangeForm

import os
from django.conf import settings


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput() 

    
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()


class Userform(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','email')

    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image',)


class ChangePasswordForm(PasswordChangeForm):

     def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user,*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'old_password',
            'new_password1',
            'new_password2',    
            Submit('submit', u'Submit', css_class='button-cards'),
            HTML('<a id="user-link" class="button-cards" href="javascript:history.back()">back</a>'),
            
    )



class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ('body',)

    
    def __init__(self, *args, **kwargs):
        super(MovieReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'body',
            Submit('submit', u'Send', css_class='button-cards'),
            HTML('<a id="user-link" class="button-cards" href="javascript:history.back()">back</a>'),
        )
        

class PersonReviewForm(forms.ModelForm):
    class Meta:
        model = PersonReview
        fields = ('body',)

    
    def __init__(self, *args, **kwargs):
        super(PersonReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'body',
            Submit('submit', u'Send', css_class='button-cards'),
            HTML('<a id="user-link" class="button-cards" href="javascript:history.back()">back</a>'),
        )

   
