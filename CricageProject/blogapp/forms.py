from django import forms
from blogapp.models import Comment
from .models import User
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)



class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
