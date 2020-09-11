from django import forms
from blogapp.models import Comment
from .models import User,AcademyUser



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)



class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']

class AcademyUserForm(forms.ModelForm):
    class Meta:
        model=AcademyUser
        fields="__all__"
