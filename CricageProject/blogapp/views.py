from django.shortcuts import render,get_object_or_404
from .models import Article
from django.contrib.auth.decorators import login_required
from blogapp import forms
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect


# Create your views here.
def homepageview(request):
    return render(request,'blogapp/index.html')


def all_post(request):
    posts = Article.objects.filter(type="news")
    bio = Article.objects.filter(type="bio")
    return render(request,'blogapp/home.html',{'posts':posts,'bio':bio})

@login_required
def post_detail(request,id):
    post = get_object_or_404(Article,id=id)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=="POST":
        form=forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=forms.CommentForm()
    return render(request,'blogapp/post_detail.html',{'post':post,'form':form,'comments':comments,'csubmit':csubmit})


def sign_up_view(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/accounts/login')
    return render(request, 'blogapp/signup.html', {'form': form})


@login_required
def academy_view(request):
    return render(request,'blogapp/academy_home.html')
